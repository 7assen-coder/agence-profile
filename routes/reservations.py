from flask import Blueprint, jsonify, request
from db import get_db
import pymysql

bp_resa = Blueprint("reservations", __name__)

@bp_resa.post("/bloquer")
def bloquer_place():
    data = request.get_json(silent=True) or {}
    id_client = data.get("id_client")
    id_place  = data.get("id_place")
    id_trajet = data.get("id_trajet")

    if not all([id_client, id_place, id_trajet]):
        return jsonify({"erreur": "id_client, id_place et id_trajet requis"}), 400

    try:
        with get_db() as (conn, cur):
            # Vérifier trajet + place
            cur.execute("""
                SELECT t.id_trajet FROM trajets t
                JOIN places p ON p.id_bus = t.id_bus
                WHERE t.id_trajet = %s AND p.id_place = %s
            """, (id_trajet, id_place))
            if not cur.fetchone():
                return jsonify({"erreur": "Trajet ou place invalide"}), 404

            # VERROU ANTI-CONFLIT
            cur.execute("""
                SELECT id_reservation, statut,
                       TIMESTAMPDIFF(MINUTE, date_reservation, NOW()) AS minutes
                FROM reservations
                WHERE id_place = %s AND id_trajet = %s AND statut != 'annulee'
                FOR UPDATE
            """, (id_place, id_trajet))
            existing = cur.fetchone()

            if existing:
                if existing["statut"] == "confirmee":
                    return jsonify({"erreur": "Place déjà confirmée", "code": "PLACE_CONFIRMEE"}), 409
                if existing["statut"] == "en_attente":
                    if existing["minutes"] < 5:
                        return jsonify({
                            "erreur": "Place bloquée par un autre client",
                            "code": "PLACE_BLOQUEE",
                            "expire_dans_minutes": 5 - existing["minutes"]
                        }), 409
                    else:
                        cur.execute("UPDATE reservations SET statut='annulee' WHERE id_reservation=%s",
                                    (existing["id_reservation"],))

            cur.execute("""
                INSERT INTO reservations (id_client, id_place, id_trajet, statut)
                VALUES (%s, %s, %s, 'en_attente')
            """, (id_client, id_place, id_trajet))
            id_reservation = cur.lastrowid

        return jsonify({
            "message": "Place bloquée — 5 minutes pour payer",
            "id_reservation": id_reservation,
            "statut": "en_attente"
        }), 201

    except pymysql.err.OperationalError as e:
        if e.args[0] == 1213:
            return jsonify({"erreur": "Conflit simultané, réessayez", "code": "DEADLOCK"}), 409
        raise


@bp_resa.post("/confirmer/<int:id_reservation>")
def confirmer_reservation(id_reservation):
    data = request.get_json(silent=True) or {}
    id_paiement = data.get("id_paiement")
    if not id_paiement:
        return jsonify({"erreur": "id_paiement requis"}), 400

    with get_db() as (conn, cur):
        cur.execute("""
            SELECT statut, TIMESTAMPDIFF(MINUTE, date_reservation, NOW()) AS minutes
            FROM reservations WHERE id_reservation = %s FOR UPDATE
        """, (id_reservation,))
        resa = cur.fetchone()
        if not resa:
            return jsonify({"erreur": "Réservation introuvable"}), 404
        if resa["statut"] != "en_attente":
            return jsonify({"erreur": f"Statut invalide : {resa['statut']}"}), 409
        if resa["minutes"] >= 5:
            cur.execute("UPDATE reservations SET statut='annulee' WHERE id_reservation=%s", (id_reservation,))
            return jsonify({"erreur": "Blocage expiré, recommencez", "code": "EXPIRE"}), 409

        cur.execute("SELECT statut FROM paiements WHERE id_paiement = %s", (id_paiement,))
        paiement = cur.fetchone()
        if not paiement or paiement["statut"] != "confirme":
            return jsonify({"erreur": "Paiement non confirmé"}), 400

        cur.execute("""
            UPDATE reservations SET statut='confirmee', id_paiement=%s
            WHERE id_reservation=%s
        """, (id_paiement, id_reservation))

    return jsonify({"message": "Réservation confirmée", "id_reservation": id_reservation})


@bp_resa.delete("/<int:id_reservation>")
def annuler_reservation(id_reservation):
    with get_db() as (conn, cur):
        cur.execute("""
            UPDATE reservations SET statut='annulee'
            WHERE id_reservation=%s AND statut != 'annulee'
        """, (id_reservation,))
        if cur.rowcount == 0:
            return jsonify({"erreur": "Introuvable ou déjà annulée"}), 404
    return jsonify({"message": "Réservation annulée", "id_reservation": id_reservation})


@bp_resa.post("/nettoyer")
def nettoyer():
    with get_db() as (conn, cur):
        cur.execute("""
            UPDATE reservations SET statut='annulee'
            WHERE statut='en_attente'
              AND date_reservation < NOW() - INTERVAL 5 MINUTE
        """)
        n = cur.rowcount
    return jsonify({"message": f"{n} blocage(s) libéré(s)"})