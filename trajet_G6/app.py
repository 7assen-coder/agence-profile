from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="trajets_saas"
    )


app = Flask(__name__)


# ── Liste des trajets ────────────────────────────────────────────────────────
@app.route('/')
@app.route('/trajets')
def liste_trajets():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.id_trajet,
            t.date_trajet,
            t.periode,
            t.heure_depart,
            t.heure_arrivee,
            t.prix,
            vd.nom  AS ville_depart,
            va.nom  AS ville_arrivee,
            a.nom   AS agence_nom,
            b.capacite
        FROM trajets t
        LEFT JOIN villes  vd ON vd.id_ville  = t.id_ville_depart
        LEFT JOIN villes  va ON va.id_ville  = t.id_ville_arrivee
        LEFT JOIN agences a  ON a.id_agence  = t.id_agence
        LEFT JOIN bus     b  ON b.id_bus     = t.id_bus
        ORDER BY t.id_trajet DESC
    """)

    trajets = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('liste_trajets.html', trajets=trajets)
# ── Créer un trajet ──────────────────────────────────────────────────────────
@app.route('/add_trajet', methods=['GET', 'POST'])
def add_trajet():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        id_agence       = request.form['id_agence']
        id_bus          = request.form['id_bus']
        id_ville_depart = request.form['id_ville_depart']
        id_ville_arrivee = request.form['id_ville_arrivee']
        date_trajet     = "25/6/2026"
        periode         = "matin"
        heure_depart    = "10:00"
        heure_arrivee   = "14:24"
        prix            = 1000

        query = """
        INSERT INTO trajets
        (id_agence, id_bus, id_ville_depart, id_ville_arrivee,
         date_trajet, periode, heure_depart, heure_arrivee, prix)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            id_agence, id_bus, id_ville_depart, id_ville_arrivee,
            date_trajet, periode, heure_depart, heure_arrivee, prix
        ))

        conn.commit()
        cursor.close()
        conn.close()
        # Rediriger vers la liste après création
        return redirect(url_for('liste_trajets'))

    # Charger les données pour les selects
    cursor.execute("SELECT * FROM agences")
    agences = cursor.fetchall()

    cursor.execute("SELECT * FROM bus")
    bus = cursor.fetchall()

    cursor.execute("SELECT * FROM villes")
    villes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', agences=agences, bus=bus, villes=villes)


if __name__ == '__main__':
    app.run(debug=True)