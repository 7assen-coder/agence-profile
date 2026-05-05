from app.db import get_connection

def lister_villes():
    """Retourne la liste de toutes les villes."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id_ville, nom, region FROM villes ORDER BY nom")
    villes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return villes


def rechercher_trajets(ville_depart=None, ville_arrivee=None,
                       date=None, periode=None,
                       agence=None, prix_max=None, tri="heure_depart"):
    """
    Recherche les trajets selon les filtres fournis.
    Tous les filtres sont optionnels.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT
            t.id_trajet,
            t.date_trajet,
            t.periode,
            t.heure_depart,
            t.heure_arrivee,
            t.prix,
            vd.nom AS ville_depart,
            va.nom AS ville_arrivee,
            a.nom  AS agence,
            b.immatriculation
        FROM trajets t
        JOIN villes vd ON t.id_ville_depart  = vd.id_ville
        JOIN villes va ON t.id_ville_arrivee = va.id_ville
        JOIN agences a  ON t.id_agence       = a.id_agence
        JOIN bus b      ON t.id_bus          = b.id_bus
        WHERE 1=1
    """

    params = []

    if ville_depart:
        sql += " AND vd.nom = %s"
        params.append(ville_depart)

    if ville_arrivee:
        sql += " AND va.nom = %s"
        params.append(ville_arrivee)

    if date:
        sql += " AND t.date_trajet = %s"
        params.append(date)

    if periode:
        sql += " AND t.periode = %s"
        params.append(periode)

    if agence:
        sql += " AND a.nom = %s"
        params.append(agence)

    if prix_max:
        sql += " AND t.prix <= %s"
        params.append(prix_max)

    tris = {
        "heure_depart": "t.heure_depart ASC",
        "prix_asc":     "t.prix ASC",
        "prix_desc":    "t.prix DESC",
    }
    sql += f" ORDER BY {tris.get(tri, 't.heure_depart ASC')}"

    cursor.execute(sql, params)
    trajets = cursor.fetchall()

    cursor.close()
    conn.close()

    for t in trajets:
        t["date_trajet"]   = str(t["date_trajet"])
        t["heure_depart"]  = str(t["heure_depart"])  if t["heure_depart"]  else None
        t["heure_arrivee"] = str(t["heure_arrivee"]) if t["heure_arrivee"] else None
        t["prix"]          = float(t["prix"])

    return trajets


def detail_trajet(id_trajet):
    """Retourne les détails complets d'un trajet."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT
            t.id_trajet,
            t.date_trajet,
            t.periode,
            t.heure_depart,
            t.heure_arrivee,
            t.prix,
            vd.nom AS ville_depart,
            va.nom AS ville_arrivee,
            a.nom  AS agence,
            a.telephone AS agence_telephone,
            b.immatriculation,
            b.capacite
        FROM trajets t
        JOIN villes vd ON t.id_ville_depart  = vd.id_ville
        JOIN villes va ON t.id_ville_arrivee = va.id_ville
        JOIN agences a  ON t.id_agence       = a.id_agence
        JOIN bus b      ON t.id_bus          = b.id_bus
        WHERE t.id_trajet = %s
    """
    cursor.execute(sql, (id_trajet,))
    trajet = cursor.fetchone()

    cursor.close()
    conn.close()

    if trajet:
        trajet["date_trajet"]   = str(trajet["date_trajet"])
        trajet["heure_depart"]  = str(trajet["heure_depart"])  if trajet["heure_depart"]  else None
        trajet["heure_arrivee"] = str(trajet["heure_arrivee"]) if trajet["heure_arrivee"] else None
        trajet["prix"]          = float(trajet["prix"])

    return trajet