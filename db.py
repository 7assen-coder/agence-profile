import pymysql
import pymysql.cursors
from contextlib import contextmanager

DB_CONFIG = {
    "host":        "localhost",
    "user":        "root",
    "password":    "",        # ← mettez votre mot de passe MySQL ici
    "database":    "transport_reservation",
    "charset":     "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit":  False,
}

@contextmanager
def get_db():
    conn = pymysql.connect(**DB_CONFIG)
    cur  = conn.cursor()
    try:
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()