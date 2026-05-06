from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Autorise les requêtes entre le port 5000, 5001 et Live Server

# ============================================================
# CONFIGURATION
# ============================================================
MOCK_BANKILY_URL = "http://localhost:5001"

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",
    "database": "transport_reservation"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ============================================================
# ROUTE : Page d'accueil (Interface Groupe 15)
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")

# ============================================================
# ROUTE PRINCIPALE : Soumettre un paiement & Confirmer (G15 + G16)
# ============================================================
@app.route("/paiement/soumettre", methods=["POST"])
def soumettre_paiement():
    # 1. Récupérer les données
    id_reservation   = request.json.get("id_reservation")
    numero_bankily   = request.json.get("numero_bankily")
    code_transaction = request.json.get("code_transaction")

    if not all([id_reservation, numero_bankily, code_transaction]):
        return jsonify({"success": False, "error": "Champs manquants"}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        # 2. Vérifier la réservation et récupérer le prix (Jointure avec trajets)
        cursor.execute("""
            SELECT r.id_client, r.statut, t.prix
            FROM   reservations r
            JOIN   trajets t ON r.id_trajet = t.id_trajet
            WHERE  r.id_reservation = %s
        """, (id_reservation,))
        resa = cursor.fetchone()

        if not resa:
            return jsonify({"success": False, "error": "Réservation introuvable"}), 404

        if resa["statut"] == "confirmee":
            return jsonify({"success": False, "error": "Cette réservation est déjà confirmée"}), 400

        # 3. Appel au Mock Bankily pour vérification réelle
        bankily_response = requests.post(
            f"{MOCK_BANKILY_URL}/bankily/verify",
            json={
                "numero_client":    numero_bankily,
                "montant":          float(resa["prix"]),
                "code_transaction": code_transaction
            },
            timeout=5
        )
        bankily_data = bankily_response.json()

        # 4. Traitement du résultat Bankily
        if bankily_data.get("verified"):
            # --- ACTION A : Enregistrer le paiement (G15) ---
            cursor.execute("""
                INSERT INTO paiements (id_client, montant, mode_paiement, statut, date_paiement)
                VALUES (%s, %s, 'mobile_money', 'confirme', %s)
            """, (resa["id_client"], resa["prix"], datetime.now()))
            id_paiement = cursor.lastrowid

            # --- ACTION B : Confirmer la réservation (G16) ---
            cursor.execute("""
                UPDATE reservations SET statut = 'confirmee' WHERE id_reservation = %s
            """, (id_reservation,))

            # --- ACTION C : Créer une notification (Email simulé) ---
            msg = f"Paiement #{id_paiement} validé. Votre voyage pour la réservation #{id_reservation} est confirmé."
            cursor.execute("""
                INSERT INTO notifications (id_reservation, message, date_envoi)
                VALUES (%s, %s, %s)
            """, (id_reservation, msg, datetime.now()))

            db.commit() # On valide tout en une seule transaction

            return jsonify({
                "success": True,
                "id_paiement": id_paiement,
                "id_reservation": id_reservation,
                "statut": "confirmee",
                "message": "Paiement réussi et réservation confirmée !"
            }), 200

        else:
            # En cas d'échec du paiement côté Bankily
            cursor.execute("""
                INSERT INTO paiements (id_client, montant, mode_paiement, statut, date_paiement)
                VALUES (%s, %s, 'mobile_money', 'echoue', %s)
            """, (resa["id_client"], resa["prix"], datetime.now()))
            db.commit()
            return jsonify({"success": False, "error": bankily_data.get("error", "Échec Bankily")}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# ============================================================
# ROUTE : Voir le statut d'un paiement
# ============================================================
@app.route("/paiement/statut/<int:id_paiement>", methods=["GET"])
def voir_statut(id_paiement):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paiements WHERE id_paiement = %s", (id_paiement,))
    paiement = cursor.fetchone()
    cursor.close()
    db.close()
    if paiement:
        paiement['date_paiement'] = paiement['date_paiement'].strftime("%Y-%m-%d %H:%M:%S")
        return jsonify(paiement), 200
    return jsonify({"erreur": "Paiement introuvable"}), 404

# ============================================================
# ROUTE : Historique des paiements
# ============================================================
@app.route("/paiement/historique/<int:id_client>", methods=["GET"])
def voir_historique(id_client):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paiements WHERE id_client = %s ORDER BY date_paiement DESC", (id_client,))
    historique = cursor.fetchall()
    for p in historique:
        p['date_paiement'] = p['date_paiement'].strftime("%Y-%m-%d %H:%M:%S")
    cursor.close()
    db.close()
    return jsonify(historique), 200

if __name__ == "__main__":
    print("=" * 50)
    print("  SERVEUR INTÉGRÉ G15 & G16 LANCÉ")
    print("  URL: http://localhost:5000")
    print("=" * 50)
    app.run(port=5000, debug=True)