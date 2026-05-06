# 1. Importation des outils nécessaires
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# 2. Configuration de la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'transport_reservation'
app.config['MYSQL_PORT'] = 3307 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('historique.html')

# FORMULAIRE DE CONNEXION CLIENT
@app.route('/login')
def login():
    return render_template('login_client.html')

@app.route('/login_check', methods=['POST'])
def login_check():
    id_client = request.form.get('id_client')
    return redirect(url_for('vue_client', id_client=id_client))

# HISTORIQUE CLIENT
@app.route('/client/<int:id_client>')
def vue_client(id_client):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT r.id_reservation, r.date_reservation, r.statut, 
               v_dep.nom AS depart, v_arr.nom AS arrivee, t.prix,
               c.nom AS passager -- Ajoutez ceci si vous voulez afficher le nom
        FROM reservations r
        JOIN clients c ON r.id_client = c.id_client
        JOIN trajets t ON r.id_trajet = t.id_trajet
        JOIN villes v_dep ON t.id_ville_depart = v_dep.id_ville
        JOIN villes v_arr ON t.id_ville_arrivee = v_arr.id_ville
        WHERE r.id_client = %s
    """, (id_client,))
    donnees = cur.fetchall()
    cur.close()
    
    # MODIFICATION : On utilise 'res' pour correspondre à votre HTML
    return render_template('historique.html', res=donnees, titre="Mon Historique (Client)")

# SUIVI AGENCE
@app.route('/agence/historique')
def vue_agence():
    id_agence = request.form.get('id_agence') or request.args.get('id_agence')
    
    if not id_agence:
        return redirect('/login-agence')

    # On récupère les deux dates
    f_date_debut = request.args.get('date_debut')
    f_date_fin = request.args.get('date_fin')
    f_statut = request.args.get('statut_filter')

    cur = mysql.connection.cursor()
    
    query = """
        SELECT c.nom AS passager, v1.nom AS depart, v2.nom AS arrivee, 
               t.date_trajet, t.prix, r.statut, r.id_reservation
        FROM reservations r
        JOIN clients c ON r.id_client = c.id_client
        JOIN trajets t ON r.id_trajet = t.id_trajet
        JOIN villes v1 ON t.id_ville_depart = v1.id_ville
        JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
        WHERE t.id_agence = %s
    """
    params = [id_agence]

    # LOGIQUE DE FILTRAGE ENTRE DEUX DATES
    if f_date_debut and f_date_fin:
        query += " AND t.date_trajet BETWEEN %s AND %s"
        params.append(f_date_debut)
        params.append(f_date_fin)
    elif f_date_debut:
        query += " AND t.date_trajet >= %s"
        params.append(f_date_debut)
    elif f_date_fin:
        query += " AND t.date_trajet <= %s"
        params.append(f_date_fin)
    
    if f_statut and f_statut != 'Tous':
        query += " AND r.statut = %s"
        params.append(f_statut)

    cur.execute(query, params)
    reservations = cur.fetchall()
    
    return render_template('recherche.html', res=reservations, id_agence=id_agence)

# ACTION : MODIFIER LE STATUT
# On ajoute <int:id_agence> dans la route pour savoir qui rediriger
@app.route('/modifier/<int:id_agence>/<int:id_res>/<statut>')
def modifier_statut(id_agence, id_res, statut):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE reservations SET statut = %s WHERE id_reservation = %s", (statut, id_res))
    mysql.connection.commit() 
    cur.close()
    # La redirection vers l'historique avec le bon ID d'agence
    return redirect(url_for('vue_agence', id_agence=id_agence))
@app.route('/login-agence')
def login_agence():
    return render_template('login_agence.html')
@app.route('/login_agence_check', methods=['POST'])
def login_agence_check():
    # 1. On récupère l'ID agence envoyé par le formulaire
    id_agence = request.form.get('id_agence')
    
    # 2. On redirige vers la page de l'historique en passant cet ID
    # url_for utilisera ta fonction 'vue_agence'
    return redirect(url_for('vue_agence', id_agence=id_agence))


if __name__ == '__main__':
    app.run(debug=True)