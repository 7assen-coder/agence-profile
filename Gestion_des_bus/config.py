# config.py
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        # ← adapter
        database="transport_db"
    )
