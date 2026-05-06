from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string
from datetime import datetime

app = Flask(__name__)

# ============================================================
# FAUSSE BASE DE DONNÉES BANKILY
# Simule des transactions déjà existantes pour tester
# ============================================================
fake_transactions = {
    "BNK-TEST-001": {
        "code": "BNK-TEST-001",
        "expediteur": "22001234",
        "montant": 500.00,
        "date": "2026-05-01T10:00:00",
        "statut": "completed"
    },
    "BNK-TEST-002": {
        "code": "BNK-TEST-002",
        "expediteur": "22005678",
        "montant": 750.00,
        "date": "2026-05-01T11:00:00",
        "statut": "completed"
    },
    "BNK-TEST-003": {
        "code": "BNK-TEST-003",
        "expediteur": "22009999",
        "montant": 300.00,
        "date": "2026-05-01T12:00:00",
        "statut": "failed"  # Pour tester le cas d'échec
    }
}

# Codes déjà utilisés (pour éviter double confirmation)
used_codes = set()


# ============================================================
# ENDPOINT 1 : Vérifier une transaction
# POST /bankily/verify
# ============================================================
@app.route("/bankily/verify", methods=["POST"])
def verify_transaction():
    data = request.get_json()

    # Champs obligatoires
    numero_client   = data.get("numero_client")
    montant_attendu = data.get("montant")
    code_transaction = data.get("code_transaction")

    # Validation basique
    if not numero_client or not montant_attendu or not code_transaction:
        return jsonify({
            "success": False,
            "error": "Champs manquants : numero_client, montant, code_transaction"
        }), 400

    # Vérifier si le code a déjà été utilisé
    if code_transaction in used_codes:
        return jsonify({
            "success": False,
            "verified": False,
            "error": "Ce code transaction a déjà été utilisé"
        }), 200

    # ── Cas 1 : transaction connue dans nos fausses données ──
    if code_transaction in fake_transactions:
        transaction = fake_transactions[code_transaction]

        # Transaction échouée
        if transaction["statut"] == "failed":
            return jsonify({
                "success": True,
                "verified": False,
                "error": "Transaction échouée côté Bankily"
            }), 200

        # Vérifier numéro client
        if transaction["expediteur"] != numero_client:
            return jsonify({
                "success": True,
                "verified": False,
                "error": "Le numéro Bankily ne correspond pas"
            }), 200

        # Vérifier montant (tolérance de ±1 MRU)
        if abs(transaction["montant"] - float(montant_attendu)) > 1:
            return jsonify({
                "success": True,
                "verified": False,
                "error": f"Montant incorrect. Reçu: {transaction['montant']} MRU"
            }), 200

        # ✅ Tout est bon
        used_codes.add(code_transaction)
        return jsonify({
            "success": True,
            "verified": True,
            "transaction": {
                "code": transaction["code"],
                "expediteur": transaction["expediteur"],
                "montant": transaction["montant"],
                "date": transaction["date"]
            }
        }), 200

    # ── Cas 2 : transaction inconnue → simulation aléatoire ──
    # 85% succès, 15% échec (pour tester les deux cas)
    if random.random() < 0.85:
        used_codes.add(code_transaction)
        return jsonify({
            "success": True,
            "verified": True,
            "transaction": {
                "code": code_transaction,
                "expediteur": numero_client,
                "montant": float(montant_attendu),
                "date": datetime.now().isoformat()
            }
        }), 200
    else:
        return jsonify({
            "success": True,
            "verified": False,
            "error": "Transaction introuvable dans le système Bankily"
        }), 200


# ============================================================
# ENDPOINT 2 : Générer un faux reçu (pour tester facilement)
# GET /bankily/generate?numero=22001234&montant=500
# ============================================================
@app.route("/bankily/generate", methods=["GET"])
def generate_fake_receipt():
    numero  = request.args.get("numero", "22001234")
    montant = request.args.get("montant", "500")

    # Générer un faux code transaction
    code = "BNK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Sauvegarder dans nos fausses données
    fake_transactions[code] = {
        "code": code,
        "expediteur": numero,
        "montant": float(montant),
        "date": datetime.now().isoformat(),
        "statut": "completed"
    }

    return jsonify({
        "success": True,
        "message": "Faux reçu généré pour les tests",
        "recu": {
            "code_transaction": code,
            "numero_expediteur": numero,
            "montant": float(montant),
            "date": datetime.now().isoformat()
        }
    }), 200


# ============================================================
# ENDPOINT 3 : Health check
# GET /bankily/status
# ============================================================
@app.route("/bankily/status", methods=["GET"])
def status():
    return jsonify({
        "service": "Mock Bankily API",
        "status": "running",
        "version": "1.0.0",
        "note": "Ceci est une simulation - pas la vraie API Bankily"
    }), 200


if __name__ == "__main__":
    print("=" * 50)
    print("  MOCK BANKILY API - Groupe 15")
    print("  http://localhost:5001")
    print("=" * 50)
    app.run(port=5001, debug=True)