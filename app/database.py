import mysql.connector
from mysql.connector import Error
from flask import g, current_app


def get_db():
    """Retourne la connexion MySQL pour la requête en cours."""
    if "db" not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config["DB_HOST"],
                user=current_app.config["DB_USER"],
                password=current_app.config["DB_PASSWORD"],
                database=current_app.config["DB_NAME"],
                charset="utf8mb4",
                autocommit=False,
            )
        except Error as e:
            raise RuntimeError(f"Impossible de se connecter à la base : {e}")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)
