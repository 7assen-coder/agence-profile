"""
Groupe 20 – Module : Statistiques (revenus + taux de remplissage)
Matricules : 251057 - 251092 - 251284
Flask + MySQL · API REST JSON
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
CORS(app)

# ─── Configuration DB ───────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "transport_reservation"),
    "charset":  "utf8mb4",
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def db_query(sql, params=None, fetchone=False):
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    result = cur.fetchone() if fetchone else cur.fetchall()
    cur.close()
    conn.close()
    return result

# ─── Helper : réponse JSON standard ─────────────────────────────────────────
def ok(data, status=200):
    return jsonify({"success": True,  "data": data}), status

def err(msg, status=400):
    return jsonify({"success": False, "error": msg}), status

# ════════════════════════════════════════════════════════════════════════════
#  PAGE HTML (dashboard frontend)
# ════════════════════════════════════════════════════════════════════════════
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ════════════════════════════════════════════════════════════════════════════
#  1. REVENUS
# ════════════════════════════════════════════════════════════════════════════

@app.route("/api/stats/revenus", methods=["GET"])
def revenus_global():
    """
    Revenus totaux (paiements confirmés).
    Paramètres optionnels : date_debut, date_fin, id_agence, periode
    """
    date_debut  = request.args.get("date_debut")
    date_fin    = request.args.get("date_fin")
    id_agence   = request.args.get("id_agence")
    periode     = request.args.get("periode")  # 'matin' | 'apres-midi'

    conditions = ["p.statut = 'confirme'"]
    params     = []

    if date_debut:
        conditions.append("DATE(p.date_paiement) >= %s")
        params.append(date_debut)
    if date_fin:
        conditions.append("DATE(p.date_paiement) <= %s")
        params.append(date_fin)
    if id_agence:
        conditions.append("t.id_agence = %s")
        params.append(id_agence)
    if periode:
        conditions.append("t.periode = %s")
        params.append(periode)

    where = " AND ".join(conditions)

    sql = f"""
        SELECT
            COALESCE(SUM(p.montant), 0)  AS revenu_total,
            COUNT(p.id_paiement)          AS nb_paiements,
            COALESCE(AVG(p.montant), 0)   AS revenu_moyen_par_reservation
        FROM paiements p
        JOIN reservations r ON r.id_paiement = p.id_paiement
        JOIN trajets      t ON t.id_trajet   = r.id_trajet
        WHERE {where}
    """
    row = db_query(sql, params, fetchone=True)
    return ok(row)


@app.route("/api/stats/revenus/par-agence", methods=["GET"])
def revenus_par_agence():
    """Revenus groupés par agence."""
    date_debut = request.args.get("date_debut")
    date_fin   = request.args.get("date_fin")

    conditions = ["p.statut = 'confirme'"]
    params     = []
    if date_debut:
        conditions.append("DATE(p.date_paiement) >= %s"); params.append(date_debut)
    if date_fin:
        conditions.append("DATE(p.date_paiement) <= %s"); params.append(date_fin)
    where = " AND ".join(conditions)

    sql = f"""
        SELECT
            a.id_agence,
            a.nom                         AS agence,
            COALESCE(SUM(p.montant), 0)   AS revenu_total,
            COUNT(r.id_reservation)       AS nb_reservations
        FROM agences a
        LEFT JOIN trajets      t ON t.id_agence   = a.id_agence
        LEFT JOIN reservations r ON r.id_trajet   = t.id_trajet
                                 AND r.statut      = 'confirmee'
        LEFT JOIN paiements    p ON p.id_paiement = r.id_paiement
                                 AND {where}
        GROUP BY a.id_agence, a.nom
        ORDER BY revenu_total DESC
    """
    return ok(db_query(sql, params))


@app.route("/api/stats/revenus/par-jour", methods=["GET"])
def revenus_par_jour():
    """Revenus jour par jour (30 derniers jours par défaut)."""
    nb_jours   = int(request.args.get("nb_jours", 30))
    id_agence  = request.args.get("id_agence")

    conditions = ["p.statut = 'confirme'",
                  "DATE(p.date_paiement) >= CURDATE() - INTERVAL %s DAY"]
    params     = [nb_jours]

    if id_agence:
        conditions.append("t.id_agence = %s"); params.append(id_agence)
    where = " AND ".join(conditions)

    sql = f"""
        SELECT
            DATE(p.date_paiement)        AS jour,
            COALESCE(SUM(p.montant), 0)  AS revenu,
            COUNT(p.id_paiement)          AS nb_reservations
        FROM paiements p
        JOIN reservations r ON r.id_paiement = p.id_paiement
        JOIN trajets      t ON t.id_trajet   = r.id_trajet
        WHERE {where}
        GROUP BY DATE(p.date_paiement)
        ORDER BY jour ASC
    """
    rows = db_query(sql, params)
    # sérialiser les dates
    for row in rows:
        if row.get("jour"):
            row["jour"] = str(row["jour"])
    return ok(rows)


@app.route("/api/stats/revenus/par-trajet", methods=["GET"])
def revenus_par_trajet():
    """Top N trajets les plus rentables."""
    limit      = int(request.args.get("limit", 10))
    id_agence  = request.args.get("id_agence")

    conditions = ["p.statut = 'confirme'"]
    params     = []
    if id_agence:
        conditions.append("t.id_agence = %s"); params.append(id_agence)
    where = " AND ".join(conditions)
    params.append(limit)

    sql = f"""
        SELECT
            t.id_trajet,
            vd.nom                       AS ville_depart,
            va.nom                       AS ville_arrivee,
            t.date_trajet,
            t.periode,
            COALESCE(SUM(p.montant), 0)  AS revenu_trajet,
            COUNT(r.id_reservation)      AS nb_reservations
        FROM trajets      t
        JOIN villes        vd ON vd.id_ville    = t.id_ville_depart
        JOIN villes        va ON va.id_ville    = t.id_ville_arrivee
        LEFT JOIN reservations r ON r.id_trajet = t.id_trajet
                                 AND r.statut   = 'confirmee'
        LEFT JOIN paiements    p ON p.id_paiement = r.id_paiement
                                 AND {where}
        GROUP BY t.id_trajet, vd.nom, va.nom, t.date_trajet, t.periode
        ORDER BY revenu_trajet DESC
        LIMIT %s
    """
    rows = db_query(sql, params)
    for row in rows:
        if row.get("date_trajet"):
            row["date_trajet"] = str(row["date_trajet"])
    return ok(rows)


@app.route("/api/stats/revenus/par-mode-paiement", methods=["GET"])
def revenus_par_mode():
    """Répartition des revenus par mode de paiement."""
    sql = """
        SELECT
            p.mode_paiement,
            COALESCE(SUM(p.montant), 0)  AS total,
            COUNT(p.id_paiement)          AS nb
        FROM paiements p
        WHERE p.statut = 'confirme'
        GROUP BY p.mode_paiement
        ORDER BY total DESC
    """
    return ok(db_query(sql))


# ════════════════════════════════════════════════════════════════════════════
#  2. TAUX DE REMPLISSAGE
# ════════════════════════════════════════════════════════════════════════════

@app.route("/api/stats/remplissage", methods=["GET"])
def remplissage_global():
    """
    Taux de remplissage global (toutes agences, tous trajets).
    taux = nb_places_confirmées / nb_places_totales × 100
    """
    date_debut = request.args.get("date_debut")
    date_fin   = request.args.get("date_fin")
    id_agence  = request.args.get("id_agence")

    cond_t = ["1=1"]
    params = []
    if date_debut:
        cond_t.append("t.date_trajet >= %s"); params.append(date_debut)
    if date_fin:
        cond_t.append("t.date_trajet <= %s"); params.append(date_fin)
    if id_agence:
        cond_t.append("t.id_agence = %s"); params.append(id_agence)
    where_t = " AND ".join(cond_t)

    sql = f"""
        SELECT
            COUNT(DISTINCT t.id_trajet)                        AS nb_trajets,
            SUM(b.capacite)                                    AS places_totales,
            COALESCE(SUM(
                (SELECT COUNT(*) FROM reservations r
                 WHERE r.id_trajet = t.id_trajet
                   AND r.statut   = 'confirmee')
            ), 0)                                              AS places_reservees,
            ROUND(
                COALESCE(SUM(
                    (SELECT COUNT(*) FROM reservations r
                     WHERE r.id_trajet = t.id_trajet
                       AND r.statut   = 'confirmee')
                ), 0) * 100.0
                / NULLIF(SUM(b.capacite), 0)
            , 2)                                               AS taux_remplissage_pct
        FROM trajets t
        JOIN bus b ON b.id_bus = t.id_bus
        WHERE {where_t}
    """
    return ok(db_query(sql, params, fetchone=True))


@app.route("/api/stats/remplissage/par-trajet", methods=["GET"])
def remplissage_par_trajet():
    """Taux de remplissage trajet par trajet."""
    date_debut = request.args.get("date_debut")
    date_fin   = request.args.get("date_fin")
    id_agence  = request.args.get("id_agence")
    limit      = int(request.args.get("limit", 20))

    conditions = ["1=1"]
    params     = []
    if date_debut:
        conditions.append("t.date_trajet >= %s"); params.append(date_debut)
    if date_fin:
        conditions.append("t.date_trajet <= %s"); params.append(date_fin)
    if id_agence:
        conditions.append("t.id_agence = %s"); params.append(id_agence)
    where = " AND ".join(conditions)
    params.append(limit)

    sql = f"""
        SELECT
            t.id_trajet,
            vd.nom                                               AS ville_depart,
            va.nom                                               AS ville_arrivee,
            t.date_trajet,
            t.periode,
            b.capacite                                           AS places_totales,
            COUNT(CASE WHEN r.statut = 'confirmee' THEN 1 END)  AS places_confirmees,
            COUNT(CASE WHEN r.statut = 'en_attente' THEN 1 END) AS places_en_attente,
            ROUND(
                COUNT(CASE WHEN r.statut = 'confirmee' THEN 1 END)
                * 100.0 / NULLIF(b.capacite, 0)
            , 2)                                                 AS taux_remplissage_pct
        FROM trajets       t
        JOIN villes        vd ON vd.id_ville   = t.id_ville_depart
        JOIN villes        va ON va.id_ville   = t.id_ville_arrivee
        JOIN bus           b  ON b.id_bus      = t.id_bus
        LEFT JOIN reservations r ON r.id_trajet = t.id_trajet
        WHERE {where}
        GROUP BY t.id_trajet, vd.nom, va.nom, t.date_trajet, t.periode, b.capacite
        ORDER BY taux_remplissage_pct DESC
        LIMIT %s
    """
    rows = db_query(sql, params)
    for row in rows:
        if row.get("date_trajet"):
            row["date_trajet"] = str(row["date_trajet"])
    return ok(rows)


@app.route("/api/stats/remplissage/par-agence", methods=["GET"])
def remplissage_par_agence():
    """Taux de remplissage moyen par agence."""
    sql = """
        SELECT
            a.id_agence,
            a.nom                                                 AS agence,
            SUM(b.capacite)                                       AS places_totales,
            COALESCE(SUM(
                (SELECT COUNT(*) FROM reservations r
                 WHERE r.id_trajet = t.id_trajet
                   AND r.statut = 'confirmee')
            ), 0)                                                  AS places_confirmees,
            ROUND(
                COALESCE(SUM(
                    (SELECT COUNT(*) FROM reservations r
                     WHERE r.id_trajet = t.id_trajet
                       AND r.statut = 'confirmee')
                ), 0) * 100.0 / NULLIF(SUM(b.capacite), 0)
            , 2)                                                   AS taux_remplissage_pct
        FROM agences a
        LEFT JOIN trajets t ON t.id_agence = a.id_agence
        LEFT JOIN bus     b ON b.id_bus    = t.id_bus
        GROUP BY a.id_agence, a.nom
        ORDER BY taux_remplissage_pct DESC
    """
    return ok(db_query(sql))


@app.route("/api/stats/remplissage/par-periode", methods=["GET"])
def remplissage_par_periode():
    """Comparaison matin vs après-midi."""
    sql = """
        SELECT
            t.periode,
            SUM(b.capacite)                                       AS places_totales,
            COALESCE(SUM(
                (SELECT COUNT(*) FROM reservations r
                 WHERE r.id_trajet = t.id_trajet
                   AND r.statut = 'confirmee')
            ), 0)                                                  AS places_confirmees,
            ROUND(
                COALESCE(SUM(
                    (SELECT COUNT(*) FROM reservations r
                     WHERE r.id_trajet = t.id_trajet
                       AND r.statut = 'confirmee')
                ), 0) * 100.0 / NULLIF(SUM(b.capacite), 0)
            , 2)                                                   AS taux_remplissage_pct
        FROM trajets t
        JOIN bus b ON b.id_bus = t.id_bus
        GROUP BY t.periode
    """
    return ok(db_query(sql))


# ════════════════════════════════════════════════════════════════════════════
#  3. SYNTHÈSE (dashboard card)
# ════════════════════════════════════════════════════════════════════════════

@app.route("/api/stats/synthese", methods=["GET"])
def synthese():
    """KPIs globaux pour le dashboard."""
    id_agence = request.args.get("id_agence")
    agence_filter = "AND t.id_agence = %s" if id_agence else ""
    params_agence = [id_agence] if id_agence else []

    # Revenus ce mois
    revenu_mois = db_query(f"""
        SELECT COALESCE(SUM(p.montant),0) AS val
        FROM paiements p
        JOIN reservations r ON r.id_paiement = p.id_paiement
        JOIN trajets      t ON t.id_trajet   = r.id_trajet
        WHERE p.statut = 'confirme'
          AND MONTH(p.date_paiement) = MONTH(CURDATE())
          AND YEAR(p.date_paiement)  = YEAR(CURDATE())
          {agence_filter}
    """, params_agence, fetchone=True)["val"]

    # Revenu total
    revenu_total = db_query(f"""
        SELECT COALESCE(SUM(p.montant),0) AS val
        FROM paiements p
        JOIN reservations r ON r.id_paiement = p.id_paiement
        JOIN trajets      t ON t.id_trajet   = r.id_trajet
        WHERE p.statut = 'confirme' {agence_filter}
    """, params_agence, fetchone=True)["val"]

    # Nb réservations confirmées
    nb_resa = db_query(f"""
        SELECT COUNT(*) AS val
        FROM reservations r
        JOIN trajets t ON t.id_trajet = r.id_trajet
        WHERE r.statut = 'confirmee' {agence_filter}
    """, params_agence, fetchone=True)["val"]

    # Taux de remplissage global
    tx = db_query(f"""
        SELECT
            ROUND(
                COALESCE(SUM(
                    (SELECT COUNT(*) FROM reservations r2
                     WHERE r2.id_trajet = t.id_trajet
                       AND r2.statut = 'confirmee')
                ),0) * 100.0 / NULLIF(SUM(b.capacite),0)
            , 2) AS val
        FROM trajets t JOIN bus b ON b.id_bus = t.id_bus
        WHERE 1=1 {agence_filter}
    """, params_agence, fetchone=True)["val"] or 0

    return ok({
        "revenu_total":      float(revenu_total),
        "revenu_ce_mois":    float(revenu_mois),
        "nb_reservations":   nb_resa,
        "taux_remplissage":  float(tx),
    })


# ─── Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
