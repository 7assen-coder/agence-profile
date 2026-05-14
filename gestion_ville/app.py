from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from conf import get_db_connection

app = Flask(__name__)
app.secret_key = "ma_cle_super_secrete" 

# ==========================================
# 1. PAGE D'ACCUEIL (LISTE DES VILLES)
# ==========================================
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) 
    cursor.execute("SELECT * FROM villes;")
    mes_villes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", villes_html=mes_villes)

# ==========================================
# 2. AJOUTER UNE VILLE
# ==========================================
@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        nom = request.form['nom']
        region = request.form['region']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO villes (nom, region) VALUES (%s, %s)", (nom, region))
        conn.commit()
        cursor.close()
        conn.close()

        flash("La ville a été ajoutée avec succès !", "success")
        return redirect(url_for('index'))

    return render_template("ajouter.html")

# ==========================================
# 3. MODIFIER UNE VILLE
# ==========================================
@app.route('/modifier/<int:id_ville>', methods=['GET', 'POST'])
def modifier(id_ville):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        nom = request.form['nom']
        region = request.form['region']
        
        cursor.execute("UPDATE villes SET nom = %s, region = %s WHERE id_ville = %s", (nom, region, id_ville))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Ville modifiée avec succès !", "success")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM villes WHERE id_ville = %s", (id_ville,))
    ville_a_modifier = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("modifier.html", ville=ville_a_modifier)

# ==========================================
# 4. SUPPRIMER UNE VILLE (VERSION FORCÉE)
# ==========================================
@app.route('/supprimer/<int:id_ville>', methods=['POST'])
def supprimer(id_ville):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Supprimer les réservations liées
        cursor.execute("""
            DELETE FROM reservations 
            WHERE id_trajet IN (
                SELECT id_trajet FROM trajets 
                WHERE id_ville_depart = %s OR id_ville_arrivee = %s
            )
        """, (id_ville, id_ville))
        
        # 2. Supprimer les trajets liés
        cursor.execute("""
            DELETE FROM trajets 
            WHERE id_ville_depart = %s OR id_ville_arrivee = %s
        """, (id_ville, id_ville))
        
        # 3. Supprimer la ville
        cursor.execute("DELETE FROM villes WHERE id_ville = %s", (id_ville,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash("La ville et ses données liées ont été supprimées !", "success")
        
    except Exception as e:
        flash(f"Erreur : {str(e)}", "error")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)