from flask import Flask, request, jsonify
from db import get_connection
from flask_cors import CORS
import bcrypt
import jwt
import datetime

app = Flask(__name__)

# Activer CORS
CORS(app)

SECRET_KEY = "transport_secret_key"
MAX_ATTEMPTS = 3


@app.route("/login", methods=["POST"])
def login():

    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    # chercher user
    cursor.execute("SELECT * FROM utilisateurs WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Utilisateur introuvable"}), 404

    # compte bloqué
    if user["is_blocked"]:
        return jsonify({"message": "Compte bloqué"}), 403

    # mot de passe incorrect
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):

        cursor.execute(
            "UPDATE utilisateurs SET attempts = attempts + 1 WHERE email=%s",
            (email,)
        )
        conn.commit()

        cursor.execute("SELECT * FROM utilisateurs WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user["attempts"] >= MAX_ATTEMPTS:
            cursor.execute(
                "UPDATE utilisateurs SET is_blocked = 1 WHERE email=%s",
                (email,)
            )
            conn.commit()

            return jsonify({"message": "Compte bloqué après 3 tentatives"}), 403

        return jsonify({
            "message": "Mot de passe incorrect",
            "attempts": user["attempts"]
        }), 401

    # reset attempts
    cursor.execute(
        "UPDATE utilisateurs SET attempts = 0 WHERE email=%s",
        (email,)
    )
    conn.commit()

    # génération token JWT
    token = jwt.encode({
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Connexion réussie",
        "token": token,
        "role": user["role"]
    })


# route protégée
@app.route("/secure")
def secure():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Token manquant"}), 403

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return jsonify({
            "message": "Accès autorisé",
            "user": decoded
        })

    except:
        return jsonify({"message": "Token invalide"}), 401


if __name__ == "__main__":
    app.run(debug=True)