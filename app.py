from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from functools import wraps


app = Flask(__name__)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',         
    'database': 'transport_db',
    'port': 3306,
    'charset': 'utf8mb4'
}

# Clé secrète pour les sessions Flask
app.config['SECRET_KEY'] = 'changez_cette_cle_secrete_en_production_2026'



def get_db_connection():
    """Crée et retourne une connexion MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erreur de connexion MySQL : {e}")
        return None


def execute_query(query, params=None, fetch=False, fetchone=False):
    """Exécute une requête SQL avec gestion automatique de la connexion."""
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
        cursor.close()
        return result
    except Error as e:
        print(f"Erreur SQL : {e}")
        conn.rollback()
        return None
    finally:
        conn.close()



def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'agent_id' not in session:
            flash("Veuillez vous connecter.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        agent = execute_query(
            "SELECT * FROM agents WHERE email=%s AND password=%s",
            (email, password), fetchone=True
        )
        if agent:
            session['agent_id'] = agent['id']
            session['agent_nom'] = f"{agent['prenom']} {agent['nom']}"
            session['agent_role'] = agent['role']
            flash(f"Bienvenue {agent['prenom']} !", "success")
            return redirect(url_for('dashboard'))
        flash("Email ou mot de passe incorrect.", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté avec succès.", "info")
    return redirect(url_for('login'))



@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    # 1. Vue globale
    total_reservations = execute_query(
        "SELECT COUNT(*) AS total FROM reservations", fetchone=True
    )['total']

    places_vendues = execute_query(
        "SELECT COUNT(*) AS total FROM reservations WHERE statut='paye'", fetchone=True
    )['total']

    capacite_globale = execute_query(
        "SELECT COALESCE(SUM(capacite_totale),0) AS total FROM trajets WHERE statut='actif'",
        fetchone=True
    )['total']

    places_disponibles = max(capacite_globale - places_vendues, 0)

    # 2. Suivi des ventes
    revenus_total = execute_query(
        "SELECT COALESCE(SUM(montant),0) AS total FROM ventes", fetchone=True
    )['total']

    ventes_par_trajet = execute_query("""
        SELECT CONCAT(t.ville_depart,' → ',t.ville_arrivee) AS trajet,
               COUNT(v.id) AS nb_ventes,
               COALESCE(SUM(v.montant),0) AS total
        FROM trajets t
        LEFT JOIN reservations r ON r.trajet_id = t.id
        LEFT JOIN ventes v ON v.reservation_id = r.id
        GROUP BY t.id
        ORDER BY total DESC
        LIMIT 10
    """, fetch=True)

    ventes_par_date = execute_query("""
        SELECT DATE(date_vente) AS jour,
               COUNT(*) AS nb_ventes,
               COALESCE(SUM(montant),0) AS total
        FROM ventes
        GROUP BY DATE(date_vente)
        ORDER BY jour DESC
        LIMIT 7
    """, fetch=True)

   
    trajets_actifs = execute_query(
        "SELECT COUNT(*) AS total FROM trajets WHERE statut='actif'", fetchone=True
    )['total']

    trajets_complets = execute_query("""
        SELECT COUNT(*) AS total FROM trajets t
        WHERE (SELECT COUNT(*) FROM reservations r
               WHERE r.trajet_id = t.id AND r.statut <> 'annule') >= t.capacite_totale
    """, fetchone=True)['total']

    trajets_disponibles = execute_query("""
        SELECT COUNT(*) AS total FROM trajets t
        WHERE t.statut='actif'
        AND (SELECT COUNT(*) FROM reservations r
             WHERE r.trajet_id = t.id AND r.statut <> 'annule') < t.capacite_totale
    """, fetchone=True)['total']

    dernieres_reservations = execute_query("""
        SELECT r.id, r.numero_place, r.statut, r.montant, r.date_reservation,
               CONCAT(c.prenom,' ',c.nom) AS client,
               CONCAT(t.ville_depart,' → ',t.ville_arrivee) AS trajet
        FROM reservations r
        JOIN clients c ON r.client_id = c.id
        JOIN trajets t ON r.trajet_id = t.id
        ORDER BY r.date_reservation DESC
        LIMIT 8
    """, fetch=True)

    stats = {
        'total_reservations': total_reservations,
        'places_vendues': places_vendues,
        'places_disponibles': places_disponibles,
        'capacite_globale': capacite_globale,
        'revenus_total': revenus_total,
        'trajets_actifs': trajets_actifs,
        'trajets_complets': trajets_complets,
        'trajets_disponibles': trajets_disponibles
    }

    return render_template('dashboard.html',
                           stats=stats,
                           ventes_par_trajet=ventes_par_trajet,
                           ventes_par_date=ventes_par_date,
                           dernieres_reservations=dernieres_reservations)



@app.route('/reservations')
@login_required
def reservations():
    statut_filtre = request.args.get('statut', '')
    recherche = request.args.get('q', '')

    query = """
        SELECT r.id, r.numero_place, r.statut, r.montant, r.date_reservation,
               c.id AS client_id, CONCAT(c.prenom,' ',c.nom) AS client,
               c.telephone,
               t.id AS trajet_id, CONCAT(t.ville_depart,' → ',t.ville_arrivee) AS trajet,
               t.date_depart, t.heure_depart
        FROM reservations r
        JOIN clients c ON r.client_id = c.id
        JOIN trajets t ON r.trajet_id = t.id
        WHERE 1=1
    """
    params = []
    if statut_filtre:
        query += " AND r.statut=%s"
        params.append(statut_filtre)
    if recherche:
        query += " AND (c.nom LIKE %s OR c.prenom LIKE %s OR c.telephone LIKE %s)"
        like = f"%{recherche}%"
        params.extend([like, like, like])
    query += " ORDER BY r.date_reservation DESC"

    liste = execute_query(query, tuple(params), fetch=True) or []

    # Stats rapides
    stats = {
        'total': len(liste),
        'payees': sum(1 for r in liste if r['statut'] == 'paye'),
        'en_attente': sum(1 for r in liste if r['statut'] == 'en_attente'),
        'annulees': sum(1 for r in liste if r['statut'] == 'annule')
    }

    return render_template('reservations.html',
                           reservations=liste, stats=stats,
                           statut_filtre=statut_filtre, recherche=recherche)


@app.route('/reservations/nouvelle', methods=['GET', 'POST'])
@login_required
def nouvelle_reservation():
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        trajet_id = request.form.get('trajet_id')
        numero_place = request.form.get('numero_place')
        statut = request.form.get('statut', 'en_attente')

        trajet = execute_query("SELECT prix FROM trajets WHERE id=%s",
                               (trajet_id,), fetchone=True)
        if not trajet:
            flash("Trajet introuvable.", "danger")
            return redirect(url_for('nouvelle_reservation'))

        montant = trajet['prix']
        agent_id = session.get('agent_id')

        new_id = execute_query("""
            INSERT INTO reservations (client_id, trajet_id, numero_place, statut, montant, agent_id)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (client_id, trajet_id, numero_place, statut, montant, agent_id))

        if new_id:
            
            if statut == 'paye':
                mode = request.form.get('mode_paiement', 'especes')
                execute_query("""
                    INSERT INTO ventes (reservation_id, montant, mode_paiement, agent_id)
                    VALUES (%s,%s,%s,%s)
                """, (new_id, montant, mode, agent_id))
            flash("Réservation créée avec succès.", "success")
            return redirect(url_for('reservations'))
        flash("Erreur lors de la création (place déjà occupée ?).", "danger")

    clients = execute_query("SELECT id, nom, prenom, telephone FROM clients ORDER BY nom",
                            fetch=True) or []
    trajets = execute_query("""
        SELECT id, ville_depart, ville_arrivee, date_depart, heure_depart, prix
        FROM trajets WHERE statut='actif' ORDER BY date_depart
    """, fetch=True) or []
    return render_template('nouvelle_reservation.html', clients=clients, trajets=trajets)


@app.route('/reservations/<int:rid>/payer', methods=['POST'])
@login_required
def payer_reservation(rid):
    mode = request.form.get('mode_paiement', 'especes')
    res = execute_query("SELECT * FROM reservations WHERE id=%s",
                        (rid,), fetchone=True)
    if not res:
        flash("Réservation introuvable.", "danger")
        return redirect(url_for('reservations'))

    execute_query("UPDATE reservations SET statut='paye' WHERE id=%s", (rid,))
    execute_query("""
        INSERT INTO ventes (reservation_id, montant, mode_paiement, agent_id)
        VALUES (%s,%s,%s,%s)
    """, (rid, res['montant'], mode, session.get('agent_id')))
    flash("Paiement enregistré.", "success")
    return redirect(url_for('reservations'))


@app.route('/reservations/<int:rid>/annuler', methods=['POST'])
@login_required
def annuler_reservation(rid):
    execute_query("UPDATE reservations SET statut='annule' WHERE id=%s", (rid,))
    flash("Réservation annulée.", "info")
    return redirect(url_for('reservations'))


@app.route('/reservations/<int:rid>/supprimer', methods=['POST'])
@login_required
def supprimer_reservation(rid):
    execute_query("DELETE FROM reservations WHERE id=%s", (rid,))
    flash("Réservation supprimée.", "warning")
    return redirect(url_for('reservations'))



@app.route('/ventes')
@login_required
def ventes():
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')
    mode = request.args.get('mode', '')

    query = """
        SELECT v.id, v.montant, v.mode_paiement, v.date_vente,
               CONCAT(c.prenom,' ',c.nom) AS client,
               CONCAT(t.ville_depart,' → ',t.ville_arrivee) AS trajet,
               r.numero_place,
               CONCAT(a.prenom,' ',a.nom) AS agent
        FROM ventes v
        JOIN reservations r ON v.reservation_id = r.id
        JOIN clients c ON r.client_id = c.id
        JOIN trajets t ON r.trajet_id = t.id
        LEFT JOIN agents a ON v.agent_id = a.id
        WHERE 1=1
    """
    params = []
    if date_debut:
        query += " AND DATE(v.date_vente) >= %s"
        params.append(date_debut)
    if date_fin:
        query += " AND DATE(v.date_vente) <= %s"
        params.append(date_fin)
    if mode:
        query += " AND v.mode_paiement=%s"
        params.append(mode)
    query += " ORDER BY v.date_vente DESC"

    liste = execute_query(query, tuple(params), fetch=True) or []

    # Statistiques
    total_revenus = sum(float(v['montant']) for v in liste)
    nb_ventes = len(liste)

    # Répartition par mode de paiement
    repartition = {}
    for v in liste:
        repartition[v['mode_paiement']] = repartition.get(v['mode_paiement'], 0) + float(v['montant'])

    # Top trajets
    top_trajets = execute_query("""
        SELECT CONCAT(t.ville_depart,' → ',t.ville_arrivee) AS trajet,
               COUNT(v.id) AS nb_ventes,
               COALESCE(SUM(v.montant),0) AS total
        FROM ventes v
        JOIN reservations r ON v.reservation_id = r.id
        JOIN trajets t ON r.trajet_id = t.id
        GROUP BY t.id
        ORDER BY total DESC
        LIMIT 5
    """, fetch=True) or []

    # Évolution des ventes (7 derniers jours)
    evolution = execute_query("""
        SELECT DATE(date_vente) AS jour,
               COALESCE(SUM(montant),0) AS total
        FROM ventes
        GROUP BY DATE(date_vente)
        ORDER BY jour DESC
        LIMIT 7
    """, fetch=True) or []

    return render_template('ventes.html',
                           ventes=liste,
                           total_revenus=total_revenus,
                           nb_ventes=nb_ventes,
                           repartition=repartition,
                           top_trajets=top_trajets,
                           evolution=evolution,
                           date_debut=date_debut, date_fin=date_fin, mode=mode)



@app.route('/trajets')
@login_required
def trajets():
    liste = execute_query("""
        SELECT t.*,
               b.immatriculation,
               (SELECT COUNT(*) FROM reservations r
                WHERE r.trajet_id = t.id AND r.statut <> 'annule') AS places_vendues
        FROM trajets t
        LEFT JOIN bus b ON t.bus_id = b.id
        ORDER BY t.date_depart DESC
    """, fetch=True) or []

    for t in liste:
        t['places_dispo'] = max(t['capacite_totale'] - t['places_vendues'], 0)
        t['taux_remplissage'] = round(
            (t['places_vendues'] / t['capacite_totale']) * 100, 1
        ) if t['capacite_totale'] > 0 else 0

    return render_template('trajets.html', trajets=liste)


@app.route('/trajets/nouveau', methods=['GET', 'POST'])
@login_required
def nouveau_trajet():
    if request.method == 'POST':
        execute_query("""
            INSERT INTO trajets (ville_depart, ville_arrivee, date_depart, heure_depart,
                                 prix, capacite_totale, bus_id, statut)
            VALUES (%s,%s,%s,%s,%s,%s,%s,'actif')
        """, (
            request.form.get('ville_depart'),
            request.form.get('ville_arrivee'),
            request.form.get('date_depart'),
            request.form.get('heure_depart'),
            request.form.get('prix'),
            request.form.get('capacite_totale'),
            request.form.get('bus_id') or None,
        ))
        flash("Trajet ajouté.", "success")
        return redirect(url_for('trajets'))

    bus = execute_query("SELECT * FROM bus WHERE statut='actif'", fetch=True) or []
    return render_template('nouveau_trajet.html', bus=bus)


@app.route('/clients')
@login_required
def clients():
    liste = execute_query("""
        SELECT c.*, COUNT(r.id) AS nb_reservations
        FROM clients c
        LEFT JOIN reservations r ON r.client_id = c.id
        GROUP BY c.id
        ORDER BY c.date_inscription DESC
    """, fetch=True) or []
    return render_template('clients.html', clients=liste)


@app.route('/clients/nouveau', methods=['POST'])
@login_required
def nouveau_client():
    execute_query("""
        INSERT INTO clients (nom, prenom, telephone, email, cni)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        request.form.get('nom'),
        request.form.get('prenom'),
        request.form.get('telephone'),
        request.form.get('email'),
        request.form.get('cni'),
    ))
    flash("Client ajouté.", "success")
    return redirect(url_for('clients'))


@app.route('/api/ventes_par_jour')
@login_required
def api_ventes_par_jour():
    data = execute_query("""
        SELECT DATE(date_vente) AS jour, COALESCE(SUM(montant),0) AS total
        FROM ventes
        GROUP BY DATE(date_vente)
        ORDER BY jour DESC
        LIMIT 14
    """, fetch=True) or []
    return jsonify([{'jour': str(d['jour']), 'total': float(d['total'])} for d in data])


@app.template_filter('money')
def money_filter(value):
    try:
        return f"{float(value):,.0f} FCFA".replace(",", " ")
    except (TypeError, ValueError):
        return value


@app.template_filter('datetime')
def datetime_filter(value, fmt='%d/%m/%Y %H:%M'):
    if not value:
        return ''
    if isinstance(value, str):
        return value
    return value.strftime(fmt)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
