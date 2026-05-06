from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import re

app = Flask(__name__)
app.secret_key = 'changez_cette_cle_en_production'

# ── Configuration MySQL ──────────────────────────────────────────────────────
app.config['MYSQL_HOST']        = 'localhost'
app.config['MYSQL_USER']        = 'root'        # ← Votre utilisateur MySQL
app.config['MYSQL_PASSWORD']    = ''            # ← Votre mot de passe MySQL
app.config['MYSQL_DB']          = 'transport_reservation'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# ── Helpers ──────────────────────────────────────────────────────────────────

def email_valide(email):
    return re.match(r'^[\w.-]+@[\w.-]+\.\w{2,}$', email)

def telephone_valide(tel):
    return re.match(r'^[\d+\s\-]{8,20}$', tel)

def montant_valide(val):
    try:
        return float(val) >= 0
    except (TypeError, ValueError):
        return False


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('inscription'))


@app.route('/inscription', methods=['GET'])
def inscription():
    return render_template('inscription_agence.html')


@app.route('/inscription', methods=['POST'])
def inscription_post():

    # ── Récupération ────────────────────────────────────────────────────────
    nom               = request.form.get('nom', '').strip()
    ville             = request.form.get('ville', '').strip()
    adresse           = request.form.get('adresse', '').strip()
    registre_commerce = request.form.get('registre_commerce', '').strip()
    telephone         = request.form.get('telephone', '').strip()
    email             = request.form.get('email', '').strip().lower()
    site_web          = request.form.get('site_web', '').strip()
    nom_responsable   = request.form.get('nom_responsable', '').strip()
    tel_responsable   = request.form.get('tel_responsable', '').strip()
    montant_paye      = request.form.get('montant_paye', '').strip()
    password          = request.form.get('mot_de_passe', '')
    confirmation      = request.form.get('confirmation', '')

    errors = []

    # ── Validations ──────────────────────────────────────────────────────────
    if not nom or len(nom) < 2:
        errors.append("Le nom de l'agence est requis (minimum 2 caractères).")

    if not ville:
        errors.append("La ville est requise.")

    if not adresse:
        errors.append("L'adresse est requise.")

    if not registre_commerce:
        errors.append("Le numéro de registre commercial est requis.")

    if not telephone or not telephone_valide(telephone):
        errors.append("Numéro de téléphone de l'agence invalide.")

    if not email or not email_valide(email):
        errors.append("Adresse e-mail invalide.")

    if not nom_responsable or len(nom_responsable) < 2:
        errors.append("Le nom du responsable est requis.")

    if not tel_responsable or not telephone_valide(tel_responsable):
        errors.append("Numéro de téléphone du responsable invalide.")

    if not montant_paye or not montant_valide(montant_paye):
        errors.append("Le montant payé est invalide (nombre positif requis).")

    if not password or len(password) < 6:
        errors.append("Le mot de passe doit contenir au moins 6 caractères.")

    if password != confirmation:
        errors.append("Les mots de passe ne correspondent pas.")

    if errors:
        return render_template('inscription_agence.html',
                               errors=errors, form_data=request.form)

    # ── Unicité email ────────────────────────────────────────────────────────
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_agence FROM agences WHERE email = %s", (email,))
    if cur.fetchone():
        errors.append("Cet e-mail est déjà utilisé par une autre agence.")
        cur.close()
        return render_template('inscription_agence.html',
                               errors=errors, form_data=request.form)

    # ── Insertion ────────────────────────────────────────────────────────────
    hashed_password = generate_password_hash(password)

    try:
        cur.execute("""
            INSERT INTO agences (
                nom, ville, adresse, registre_commerce,
                telephone, email, site_web,
                nom_responsable, tel_responsable,
                montant_paye, mot_de_passe, statut
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s, %s, 'en_attente'
            )
        """, (
            nom, ville, adresse, registre_commerce,
            telephone, email, site_web if site_web else None,
            nom_responsable, tel_responsable,
            float(montant_paye), hashed_password
        ))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('succes'))

    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        errors.append("Erreur serveur. Veuillez réessayer.")
        return render_template('inscription_agence.html',
                               errors=errors, form_data=request.form)


@app.route('/succes')
def succes():
    return render_template('inscription_agence.html', success=True)


if __name__ == '__main__':
    app.run(debug=True)