from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Connexion à ta base MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Mets ton mot de passe si tu en as un
        database="transport_reservation"
    )

@app.route('/')
def home():
    return "Bienvenue sur l'application de réservation !"

# Ta future route pour les tickets (mission Zeineb)
@app.route('/ticket/<int:id_res>')
def ticket(id_res):
    # C'est ici qu'on mettra la logique QR Code plus tard
    return f"Page du ticket pour la réservation n°{id_res}"

if __name__ == '__main__':
    app.run(debug=True)