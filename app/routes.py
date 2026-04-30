import mysql.connector
from mysql.connector import Error
from flask import request, jsonify

@app.route('/api/reservations', methods=['POST'])
def api_reserver():
    data = request.get_json()
    # On appelle ta fonction avec les données reçues
    succes = reserver_place(data['client_id'], data['place_id'], data['trajet_id'])
    
    if succes:
        return jsonify({"message": "Réservation réussie"}), 201
    else:
        return jsonify({"error": "Place déjà occupée"}), 400

def reserver_place(client_id, place_id, trajet_id):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='transport_reservation',
            user='root',
            password=''
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 1. Démarrer la transaction
            connection.start_transaction()

            # 2. L'ALGORITHME DE VÉRIFICATION
            # On cherche s'il existe une réservation non annulée pour ce trajet/place
            query_check = """
                SELECT id_reservation FROM reservations 
                WHERE id_place = %s AND id_trajet = %s AND statut != 'annulee'
                FOR UPDATE; -- Verrouille la ligne pendant la vérification
            """
            cursor.execute(query_check, (place_id, trajet_id))
            
            if cursor.fetchone():
                print("❌ Échec : La place est déjà occupée pour ce trajet.")
                connection.rollback() # On annule tout
                return False

            # 3. INSERTION SI DISPONIBLE
            query_insert = """
                INSERT INTO reservations (id_client, id_place, id_trajet, statut)
                VALUES (%s, %s, %s, 'confirmee');
            """
            cursor.execute(query_insert, (client_id, place_id, trajet_id))

            # 4. VALIDATION
            connection.commit()
            print("✅ Réservation confirmée !")
            return True

    except Error as e:
        if connection:
            connection.rollback()
        print(f"Erreur lors de la réservation : {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
