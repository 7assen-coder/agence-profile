import mysql.connector as mysql


DB_CONFIG = {
    'host': 'localhost',
    'user': 'MDK',
    'password': '1234',
    'database': 'transport_reservation_v4 '
}
def get_db_connection():
    try:
        return mysql.connect(**DB_CONFIG)
    except mysql.Error as e:
        print(f"Erreur MySQL: {e}")
        return None
      




def init_db():
    conn = get_db_connection()
    if conn:
        print("Base de données connectée avec succès.")
    else:
        print("Échec de la connexion à la base de données.")
    return conn
