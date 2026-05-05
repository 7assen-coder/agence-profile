from flask import Blueprint, jsonify
from db import get_db

bp_dispo = Blueprint("disponibilites", __name__)

@bp_dispo.get("/<int:id_trajet>")
def disponibilites_trajet(id_trajet):
    with get_db() as (conn, cur):
        cur.execute("SELECT * FROM trajets WHERE id_trajet = %s", (id_trajet,))
        trajet = cur.fetchone()
        if not trajet:
            return jsonify({"erreur": "Trajet introuvable"}), 404

        cur.execute("""
            SELECT
                p.id_place,
                p.numero_place,
                CASE
                    WHEN r.id_reservation IS NULL                               THEN 'libre'
                    WHEN r.statut = 'annulee'                                   THEN 'libre'
                    WHEN r.statut = 'en_attente'
                         AND r.date_reservation < NOW() - INTERVAL 5 MINUTE    THEN 'expiree'
                    WHEN r.statut = 'en_attente'                                THEN 'bloquee'
                    WHEN r.statut = 'confirmee'                                 THEN 'confirmee'
                END AS statut_place,
                CASE
                    WHEN r.statut = 'en_attente'
                         AND r.date_reservation >= NOW() - INTERVAL 5 MINUTE
                    THEN TIMESTAMPDIFF(SECOND, NOW(), r.date_reservation + INTERVAL 5 MINUTE)
                END AS secondes_restantes
            FROM places p
            LEFT JOIN reservations r
                   ON r.id_place  = p.id_place
                  AND r.id_trajet = %s
                  AND r.statut   != 'annulee'
            WHERE p.id_bus = (SELECT id_bus FROM trajets WHERE id_trajet = %s)
            ORDER BY p.numero_place
        """, (id_trajet, id_trajet))
        places = cur.fetchall()

    return jsonify({"trajet": trajet, "places": places, "total": len(places)})


@bp_dispo.get("/<int:id_trajet>/resume")
def resume_trajet(id_trajet):
    with get_db() as (conn, cur):
        cur.execute("""
            SELECT
                COUNT(p.id_place) AS total,
                SUM(CASE
                    WHEN r.id_reservation IS NULL THEN 1
                    WHEN r.statut = 'annulee'     THEN 1
                    WHEN r.statut = 'en_attente'
                         AND r.date_reservation < NOW() - INTERVAL 5 MINUTE THEN 1
                    ELSE 0
                END) AS libres,
                SUM(CASE
                    WHEN r.statut = 'en_attente'
                         AND r.date_reservation >= NOW() - INTERVAL 5 MINUTE THEN 1
                    ELSE 0
                END) AS bloquees,
                SUM(CASE WHEN r.statut = 'confirmee' THEN 1 ELSE 0 END) AS confirmees
            FROM places p
            LEFT JOIN reservations r
                   ON r.id_place  = p.id_place
                  AND r.id_trajet = %s
                  AND r.statut   != 'annulee'
            WHERE p.id_bus = (SELECT id_bus FROM trajets WHERE id_trajet = %s)
        """, (id_trajet, id_trajet))
        resume = cur.fetchone()

    return jsonify(resume)