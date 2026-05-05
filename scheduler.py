from apscheduler.schedulers.background import BackgroundScheduler
from db import get_db

def liberer_places_expirees():
    try:
        with get_db() as (conn, cur):
            cur.execute("""
                UPDATE reservations
                SET    statut = 'annulee'
                WHERE  statut = 'en_attente'
                  AND  date_reservation < NOW() - INTERVAL 5 MINUTE
            """)
    except Exception as e:
        print(f"[Scheduler] Erreur : {e}")

def demarrer_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(liberer_places_expirees, "interval", seconds=60)
    scheduler.start()
    print("[Scheduler] Démarré — nettoyage toutes les 60s")
    return scheduler