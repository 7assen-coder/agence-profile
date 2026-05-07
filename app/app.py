from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

MOCK_BANKILY_URL = "http://localhost:5001"

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",
    "database": "transport_reservation"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


# ============================================================
# ROUTE 1 : Client soumet son paiement
# POST /paiement/soumettre
# ============================================================
@app.route("/paiement/soumettre", methods=["POST"])
def soumettre_paiement():
    id_reservation   = request.json.get("id_reservation")
    mode_paiement    = request.json.get("mode_paiement")
    numero_bankily   = request.json.get("numero_bankily")
    code_transaction = request.json.get("code_transaction")

    if not all([id_reservation, mode_paiement]):
        return jsonify({"success": False, "error": "Champs manquants : id_reservation, mode_paiement"}), 400

    modes_valides = ['especes', 'carte', 'mobile_money', 'virement']
    if mode_paiement not in modes_valides:
        return jsonify({"success": False, "error": "Mode de paiement invalide"}), 400

    if mode_paiement == "mobile_money":
        if not code_transaction or not numero_bankily:
            return jsonify({
                "success": False,
                "error": "numero_bankily et code_transaction obligatoires pour mobile_money"
            }), 400
    else:
        code_transaction = None
        numero_bankily   = None

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    # Vérifier la réservation
    cursor.execute("""
        SELECT r.id_client, r.statut, t.prix
        FROM   reservations r
        JOIN   trajets t ON r.id_trajet = t.id_trajet
        WHERE  r.id_reservation = %s
    """, (id_reservation,))
    resa = cursor.fetchone()

    if not resa:
        cursor.close(); db.close()
        return jsonify({"success": False, "error": "Réservation introuvable"}), 404

    if resa["statut"] == "confirmee":
        cursor.close(); db.close()
        return jsonify({"success": False, "error": "Réservation déjà confirmée"}), 400

    # Vérifier unicité du code transaction (mobile_money seulement)
    if code_transaction:
        cursor.execute("SELECT id_paiement FROM paiements WHERE code_transaction = %s", (code_transaction,))
        if cursor.fetchone():
            cursor.close(); db.close()
            return jsonify({"success": False, "error": "Ce code transaction a déjà été utilisé"}), 409

    # ── mobile_money : appeler Bankily ──
    if mode_paiement == "mobile_money":
        try:
            bankily_resp = requests.post(
                f"{MOCK_BANKILY_URL}/bankily/verify",
                json={
                    "numero_client":    numero_bankily,
                    "montant":          float(resa["prix"]),
                    "code_transaction": code_transaction
                },
                timeout=5
            )
            bankily_data = bankily_resp.json()
        except Exception as e:
            cursor.close(); db.close()
            return jsonify({"success": False, "error": f"Bankily inaccessible : {str(e)}"}), 500

        if not bankily_data.get("verified"):
            cursor.execute("""
                INSERT INTO paiements (id_client, montant, mode_paiement, statut, date_paiement, code_transaction)
                VALUES (%s, %s, %s, 'echoue', %s, %s)
            """, (resa["id_client"], resa["prix"], mode_paiement, datetime.now(), code_transaction))
            db.commit(); cursor.close(); db.close()
            return jsonify({
                "success": False,
                "error":   bankily_data.get("error", "Paiement non vérifié par Bankily"),
                "statut":  "echoue"
            }), 200

    # ── Insérer le paiement ──
    cursor.execute("""
        INSERT INTO paiements (id_client, montant, mode_paiement, statut, date_paiement, code_transaction)
        VALUES (%s, %s, %s, 'confirmee_bankily', %s, %s)
    """, (resa["id_client"], resa["prix"], mode_paiement, datetime.now(), code_transaction))
    id_paiement = cursor.lastrowid

    # ── Lier la réservation au paiement ──
    cursor.execute("""
        UPDATE reservations
        SET id_paiement = %s
        WHERE id_reservation = %s
    """, (id_paiement, id_reservation))

    db.commit(); cursor.close(); db.close()

    msg = "Paiement confirmé par Bankily" if mode_paiement == "mobile_money" else "Paiement soumis — en attente de validation agent"

    return jsonify({
        "success":     True,
        "id_paiement": id_paiement,
        "statut":      "confirmee_bankily",
        "message":     msg
    }), 200


# ============================================================
# ROUTE 2 : Agent — liste paiements confirmés Bankily
# GET /agent/paiements
# ============================================================
@app.route("/agent/paiements", methods=["GET"])
def agent_liste():
    db     = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            p.id_paiement, p.montant, p.date_paiement,
            p.mode_paiement, p.statut, p.code_transaction,
            c.nom, c.prenom, c.telephone,
            r.id_reservation,
            vd.nom AS ville_depart,
            va.nom AS ville_arrivee,
            t.date_trajet, t.periode
        FROM paiements p
        JOIN clients      c  ON p.id_client        = c.id_client
        JOIN reservations r  ON r.id_paiement      = p.id_paiement
        JOIN trajets      t  ON r.id_trajet         = t.id_trajet
        JOIN villes       vd ON t.id_ville_depart   = vd.id_ville
        JOIN villes       va ON t.id_ville_arrivee  = va.id_ville
        WHERE p.statut = 'confirmee_bankily'
        ORDER BY p.date_paiement DESC
    """)
    paiements = cursor.fetchall()
    cursor.close(); db.close()
    return jsonify(paiements), 200


# ============================================================
# ROUTE 3 : Agent — confirmer définitivement
# POST /agent/confirmer/<id_paiement>
# ============================================================
@app.route("/agent/confirmer/<int:id_paiement>", methods=["POST"])
def agent_confirmer(id_paiement):
    db     = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT statut FROM paiements WHERE id_paiement = %s", (id_paiement,))
    paiement = cursor.fetchone()

    if not paiement:
        cursor.close(); db.close()
        return jsonify({"success": False, "error": "Paiement introuvable"}), 404

    if paiement["statut"] != "confirmee_bankily":
        cursor.close(); db.close()
        return jsonify({"success": False, "error": f"Statut invalide : {paiement['statut']}"}), 400

    cursor.execute("""
        UPDATE paiements SET statut = 'confirmee_finale'
        WHERE id_paiement = %s
    """, (id_paiement,))

    cursor.execute("""
        UPDATE reservations SET statut = 'confirmee'
        WHERE id_paiement = %s
    """, (id_paiement,))

    db.commit(); cursor.close(); db.close()

    return jsonify({"success": True, "message": "Paiement confirmé définitivement"}), 200


# ============================================================
# ROUTE 4 : Statut d'un paiement
# GET /paiement/statut/<id_paiement>
# ============================================================
@app.route("/paiement/statut/<int:id_paiement>", methods=["GET"])
def statut_paiement(id_paiement):
    db     = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id_paiement, p.montant, p.date_paiement,
               p.mode_paiement, p.statut, p.code_transaction,
               c.nom, c.prenom
        FROM paiements p
        JOIN clients c ON p.id_client = c.id_client
        WHERE p.id_paiement = %s
    """, (id_paiement,))
    paiement = cursor.fetchone()
    cursor.close(); db.close()
    if not paiement:
        return jsonify({"erreur": "Paiement introuvable"}), 404
    return jsonify(paiement), 200


# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  GROUPE 15+16 — Paiement & Confirmation")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(port=5000, debug=True)