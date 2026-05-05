from flask import Blueprint, jsonify, request
from db import get_db

bp_paiement = Blueprint("paiements", __name__)

@bp_paiement.post("/")
def creer_paiement():
    data = request.get_json(silent=True) or {}
    id_client      = data.get("id_client")
    id_reservation = data.get("id_reservation")
    montant        = data.get("montant")
    mode           = data.get("mode_paiement")

    if not all([id_client, id_reservation, montant, mode]):
        return jsonify({"erreur": "Tous les champs sont requis"}), 400

    modes_valides = {"especes", "carte", "mobile_money", "virement"}
    if mode not in modes_valides:
        return jsonify({"erreur": f"Mode invalide. Choisir : {modes_valides}"}), 400

    with get_db() as (conn, cur):
        cur.execute("""
            SELECT r.id_reservation, t.prix,
                   TIMESTAMPDIFF(MINUTE, r.date_reservation, NOW()) AS minutes
            FROM reservations r
            JOIN trajets t ON t.id_trajet = r.id_trajet
            WHERE r.id_reservation = %s AND r.id_client = %s AND r.statut = 'en_attente'
        """, (id_reservation, id_client))
        resa = cur.fetchone()

        if not resa:
            return jsonify({"erreur": "Réservation introuvable ou non autorisée"}), 404
        if resa["minutes"] >= 5:
            cur.execute("UPDATE reservations SET statut='annulee' WHERE id_reservation=%s", (id_reservation,))
            return jsonify({"erreur": "Blocage expiré, recommencez"}), 409
        if float(montant) < float(resa["prix"]):
            return jsonify({"erreur": f"Montant insuffisant. Prix : {resa['prix']} MRU"}), 400

        cur.execute("""
            INSERT INTO paiements (id_client, montant, mode_paiement, statut)
            VALUES (%s, %s, %s, 'confirme')
        """, (id_client, montant, mode))
        id_paiement = cur.lastrowid

        cur.execute("""
            UPDATE reservations SET statut='confirmee', id_paiement=%s
            WHERE id_reservation=%s
        """, (id_paiement, id_reservation))

    return jsonify({
        "message": "Paiement effectué et réservation confirmée",
        "id_paiement": id_paiement,
        "id_reservation": id_reservation,
        "statut": "confirmee"
    }), 201