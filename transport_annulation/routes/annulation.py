from flask import Blueprint, jsonify
import mysql.connector
from datetime import datetime, timedelta

annulation_bp = Blueprint('annulation', __name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transport_reservation"
    )



@annulation_bp.route('/clients/<int:id_client>/reservations', methods=['GET'])
def mes_reservations(id_client):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id_reservation, r.statut, r.date_reservation,
               t.date_trajet, t.periode, t.prix,
               t.heure_depart,
               vd.nom AS ville_depart, va.nom AS ville_arrivee,
               p.numero_place,
               CASE 
                   WHEN r.statut = 'annulee' AND r.statut_avant = 'confirmee' 
                   THEN 1 ELSE 0 
               END AS etait_confirmee
        FROM reservations r
        JOIN trajets t ON r.id_trajet = t.id_trajet
        JOIN villes vd ON t.id_ville_depart = vd.id_ville
        JOIN villes va ON t.id_ville_arrivee = va.id_ville
        JOIN places p ON r.id_place = p.id_place
        WHERE r.id_client = %s
    """, (id_client,))
    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultats), 200

@annulation_bp.route('/reservations/<int:id_reservation>/annuler', methods=['PUT'])
def annuler_reservation(id_reservation):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM reservations WHERE id_reservation = %s",
        (id_reservation,)
    )
    reservation = cursor.fetchone()

    if not reservation:
        return jsonify({"erreur": "Reservation introuvable"}), 404

    if reservation['statut'] == 'annulee':
        return jsonify({"erreur": "Deja annulee"}), 400

    rembourse = False
    montant = 0

    
    if reservation['statut'] == 'confirmee':
        cursor.execute(
            "SELECT prix FROM trajets WHERE id_trajet = %s",
            (reservation['id_trajet'],)
        )
        trajet = cursor.fetchone()
        montant = trajet['prix'] if trajet else 0
        rembourse = True

    
    cursor.execute(
        """UPDATE reservations 
           SET statut = 'annulee', 
               statut_avant = %s 
           WHERE id_reservation = %s""",
        (reservation['statut'], id_reservation,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Reservation annulee avec succes",
        "rembourse": rembourse,
        "montant": float(montant)
    }), 200



@annulation_bp.route('/reservations/annuler-non-payes', methods=['PUT'])
def annuler_non_payes():
    conn = get_connection()
    cursor = conn.cursor()
    limite = datetime.now() - timedelta(hours=24)
    cursor.execute("""
        UPDATE reservations
        SET statut = 'annulee',
            statut_avant = 'en_attente'
        WHERE statut = 'en_attente'
        AND date_reservation < %s
    """, (limite,))
    conn.commit()
    nb = cursor.rowcount
    cursor.close()
    conn.close()
    return jsonify({
        "message": f"{nb} reservation(s) annulee(s) automatiquement"
    }), 200