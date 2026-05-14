from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = 'transavis_esp_2026'

# ============================================
# CONNEXION
# ============================================
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='transport_reservation'
    )

# ============================================
# PAGES — ROUTES HTML
# ============================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/avis')
def page_avis():
    return render_template('avis.html')

@app.route('/trajets')
def page_trajets():
    return render_template('trajets.html')

@app.route('/statistiques')
def page_statistiques():
    return render_template('statistiques.html')

@app.route('/feedbacks')
def feedbacks():
    return render_template('avis.html')

# ============================================
# API — AGENCES
# ============================================
@app.route('/api/agences')
def api_agences():
    try:
        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.id_agence, a.Nom, a.Telephone,
                   ROUND(AVG(av.note_globale),1) AS note_moyenne,
                   COUNT(av.id) AS nb_avis
            FROM agences a
            LEFT JOIN trajets t  ON a.id_agence = t.id_agence
            LEFT JOIN avis    av ON t.id_trajet  = av.trajet_id
            GROUP BY a.id_agence ORDER BY a.Nom
        """)
        data = cur.fetchall()
        cur.close(); conn.close()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

@app.route('/api/agences/<int:aid>/trajets')
def api_trajets_agence(aid):
    try:
        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT t.id_trajet, t.moment_journee, t.prix,
                   v1.Nom_ville AS depart, v2.Nom_ville AS arrivee
            FROM trajets t
            LEFT JOIN villes v1 ON t.id_ville_depart  = v1.id_ville
            LEFT JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
            WHERE t.id_agence = %s
        """, (aid,))
        data = cur.fetchall()
        for r in data:
            for k, v in r.items():
                if hasattr(v, 'isoformat'): r[k] = v.isoformat()
        cur.close(); conn.close()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

# ============================================
# API — TRAJETS
# ============================================
@app.route('/api/trajets')
def api_trajets():
    try:
        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT t.id_trajet, t.moment_journee, t.prix,
                   v1.Nom_ville AS ville_depart,
                   v2.Nom_ville AS ville_arrivee,
                   a.Nom AS agence_nom,
                   ROUND(AVG(av.note_globale), 1) AS note_moyenne,
                   COUNT(av.id) AS nb_avis
            FROM trajets t
            LEFT JOIN villes  v1 ON t.id_ville_depart  = v1.id_ville
            LEFT JOIN villes  v2 ON t.id_ville_arrivee = v2.id_ville
            LEFT JOIN agences a  ON t.id_agence        = a.id_agence
            LEFT JOIN avis    av ON t.id_trajet        = av.trajet_id
            GROUP BY t.id_trajet
            ORDER BY t.id_trajet
        """)
        data = cur.fetchall()
        for r in data:
            for k, v in r.items():
                if hasattr(v, 'isoformat'): r[k] = v.isoformat()
        cur.close(); conn.close()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

# ============================================
# API — CLIENTS
# ============================================
@app.route('/api/clients')
def api_clients():
    try:
        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM clients ORDER BY nom")
        data = cur.fetchall()
        cur.close(); conn.close()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

@app.route('/api/clients', methods=['POST'])
def creer_client():
    try:
        d   = request.get_json()
        nom = d.get('nom', '').strip()
        if not nom:
            return jsonify({"ok": False, "msg": "Nom requis"}), 400
        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT id_client FROM clients WHERE nom = %s", (nom,))
        ex = cur.fetchone()
        if ex:
            cur.close(); conn.close()
            return jsonify({"ok": True, "id": ex['id_client']})
        cur2 = conn.cursor()
        cur2.execute("INSERT INTO clients (nom, telephone) VALUES (%s, %s)", (nom, ''))
        conn.commit()
        new_id = cur2.lastrowid
        cur.close(); cur2.close(); conn.close()
        return jsonify({"ok": True, "id": new_id}), 201
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

# ============================================
# API — AVIS
# ============================================
@app.route('/api/avis')
def api_avis():
    try:
        trajet_id = request.args.get('trajet')
        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        sql = """
            SELECT av.id, av.note_globale, av.commentaire,
                   av.statut, av.date_creation,
                   c.nom  AS client_nom,
                   ag.Nom AS agence_nom,
                   v1.Nom_ville AS depart,
                   v2.Nom_ville AS arrivee
            FROM avis av
            LEFT JOIN clients c  ON av.client_id  = c.id_client
            LEFT JOIN trajets t  ON av.trajet_id  = t.id_trajet
            LEFT JOIN agences ag ON t.id_agence   = ag.id_agence
            LEFT JOIN villes  v1 ON t.id_ville_depart  = v1.id_ville
            LEFT JOIN villes  v2 ON t.id_ville_arrivee = v2.id_ville
        """
        values = []
        if trajet_id:
            sql += " WHERE av.trajet_id = %s"
            values.append(trajet_id)
        sql += " ORDER BY av.date_creation DESC"
        cur.execute(sql, values)
        data = cur.fetchall()
        for r in data:
            for k, v in r.items():
                if hasattr(v, 'isoformat'): r[k] = v.isoformat()
        cur.close(); conn.close()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

@app.route('/api/avis', methods=['POST'])
def creer_avis():
    try:
        d    = request.get_json()
        cid  = d.get('client_id')
        tid  = d.get('trajet_id')
        note = d.get('note_globale')
        comm = d.get('commentaire', '')
        if not all([cid, tid, note]):
            return jsonify({"ok": False, "msg": "Champs manquants"}), 400
        if not (1 <= int(note) <= 5):
            return jsonify({"ok": False, "msg": "Note entre 1 et 5"}), 400
        conn = get_db()
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO avis
            (client_id, trajet_id, note_globale, note_trajet, note_bus,
             note_agence, note_chauffeur, commentaire, statut, date_creation)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'publie',%s)
        """, (cid, tid, note, note, note, note, note, comm, date.today().isoformat()))
        conn.commit()
        new_id = cur.lastrowid
        cur.close(); conn.close()
        return jsonify({"ok": True, "id": new_id}), 201
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

@app.route('/api/avis/<int:aid>', methods=['DELETE'])
def supprimer_avis(aid):
    try:
        conn = get_db()
        cur  = conn.cursor()
        cur.execute("DELETE FROM reponses_avis WHERE avis_id = %s", (aid,))
        cur.execute("DELETE FROM avis WHERE id = %s", (aid,))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

# ============================================
# API — RÉPONSES
# ============================================
@app.route('/api/reponses')
def api_reponses():
    try:
        aid  = request.args.get('avis_id')
        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        sql  = "SELECT * FROM reponses_avis"
        if aid: sql += " WHERE avis_id = %s"
        cur.execute(sql, (aid,) if aid else ())
        data = cur.fetchall()
        for r in data:
            for k, v in r.items():
                if hasattr(v, 'isoformat'): r[k] = v.isoformat()
        cur.close(); conn.close()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

@app.route('/api/reponses', methods=['POST'])
def creer_reponse():
    try:
        d   = request.get_json()
        aid = d.get('avis_id')
        rep = d.get('reponse', '').strip()
        if not all([aid, rep]):
            return jsonify({"ok": False, "msg": "Champs manquants"}), 400
        conn = get_db()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO reponses_avis (avis_id, reponse, date_reponse) VALUES (%s,%s,%s)",
            (aid, rep, date.today().isoformat())
        )
        conn.commit()
        new_id = cur.lastrowid
        cur.close(); conn.close()
        return jsonify({"ok": True, "id": new_id}), 201
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

# ============================================
# API — STATISTIQUES
# ============================================
@app.route('/api/statistiques')
def api_statistiques():
    try:
        conn = get_db()
        cur  = conn.cursor(dictionary=True)

        cur.execute("SELECT ROUND(AVG(note_globale),2) AS note_moyenne, COUNT(*) AS total_avis FROM avis")
        global_stats = cur.fetchone()

        cur.execute("SELECT note_globale AS note, COUNT(*) AS nombre FROM avis GROUP BY note_globale ORDER BY note_globale")
        repartition = cur.fetchall()

        cur.execute("""
            SELECT t.id_trajet, v1.Nom_ville AS depart, v2.Nom_ville AS arrivee,
                   ROUND(AVG(av.note_globale),1) AS note_moyenne, COUNT(av.id) AS nb_avis
            FROM trajets t
            LEFT JOIN villes v1 ON t.id_ville_depart  = v1.id_ville
            LEFT JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
            LEFT JOIN avis   av ON t.id_trajet        = av.trajet_id
            GROUP BY t.id_trajet HAVING nb_avis > 0
            ORDER BY note_moyenne DESC LIMIT 3
        """)
        top_trajets = cur.fetchall()

        cur.execute("SELECT COUNT(*) AS total_reponses FROM reponses_avis")
        reponses = cur.fetchone()

        cur.close(); conn.close()
        return jsonify({"ok": True, "data": {
            "global": global_stats,
            "repartition": repartition,
            "top_trajets": top_trajets,
            "reponses": reponses
        }})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

# ============================================
# LANCEMENT
# ============================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)