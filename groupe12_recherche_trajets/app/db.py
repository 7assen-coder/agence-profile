import mysql.connector
import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

def get_connection():
    """Crée et retourne une connexion à la base de données."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )