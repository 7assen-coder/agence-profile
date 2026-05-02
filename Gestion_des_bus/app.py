# app.py — Groupe 8 : Gestion des Bus
# Matricules : 251081 – 251048 – 251083
# Port : 5008

from flask import Flask, request, jsonify
from config import get_db

app = Flask(__name__)


# ─────────────────────────────────────────────────────
# POST /api/bus
# Créer un bus
# Body JSON : { "immatriculation": "MR-1234-A", "agence_id": 1 }
# ─────────────────────────────────────────────────────
@app.route('/api/bus', methods=['POST'])
def creer_bus():
    data      = request.get_json()
    immat     = data.get('immatriculation', '').strip().upper()
    agence_id = data.get('agence_id')

    if not immat or not agence_id:
        return jsonify({'erreur': 'immatriculation et agence_id sont requis'}), 400

    db  = get_db()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO bus (immatriculation, capacite, agence_id) VALUES (%s, 12, %s)",
            (immat, agence_id)
        )
        db.commit()
        return jsonify({'message': 'Bus créé', 'bus_id': cur.lastrowid}), 201

    except Exception as e:
        db.rollback()
        return jsonify({'erreur': str(e)}), 400
    finally:
        cur.close(); db.close()


# ─────────────────────────────────────────────────────
# GET /api/bus
# Lister tous les bus
# ─────────────────────────────────────────────────────
@app.route('/api/bus', methods=['GET'])
def lister_bus():
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT b.id, b.immatriculation, b.capacite,
               b.agence_id, a.nom AS agence_nom,
               b.trajet_id
        FROM bus b
        JOIN agences a ON a.id = b.agence_id
        ORDER BY b.id
    """)
    result = cur.fetchall()
    cur.close(); db.close()
    return jsonify(result), 200


# ─────────────────────────────────────────────────────
# POST /api/bus/<bus_id>/assigner/<trajet_id>
# Associer un bus à un trajet (capacité = 12 imposée)
# Groupe 9 lit cette association pour générer les places
# ─────────────────────────────────────────────────────
@app.route('/api/bus/<int:bus_id>/assigner/<int:trajet_id>', methods=['POST'])
def assigner_bus(bus_id, trajet_id):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    try:
        # Vérifier que le bus existe
        cur.execute("SELECT id, trajet_id FROM bus WHERE id = %s", (bus_id,))
        bus = cur.fetchone()
        if not bus:
            return jsonify({'erreur': 'Bus introuvable'}), 404

        # Vérifier que le bus n'est pas déjà assigné
        if bus['trajet_id'] is not None:
            return jsonify({'erreur': 'Ce bus est déjà assigné à un trajet'}), 409

        # Vérifier que le trajet existe
        cur.execute("SELECT id FROM trajets WHERE id = %s", (trajet_id,))
        if not cur.fetchone():
            return jsonify({'erreur': 'Trajet introuvable'}), 404

        # Vérifier qu'aucun autre bus n'est déjà assigné à ce trajet
        cur.execute("SELECT id FROM bus WHERE trajet_id = %s", (trajet_id,))
        if cur.fetchone():
            return jsonify({'erreur': 'Ce trajet a déjà un bus assigné'}), 409

        # Assigner le bus au trajet
        cur.execute(
            "UPDATE bus SET trajet_id = %s WHERE id = %s",
            (trajet_id, bus_id)
        )
        db.commit()

        return jsonify({
            'message'   : 'Bus assigné au trajet',
            'bus_id'    : bus_id,
            'trajet_id' : trajet_id,
            'capacite'  : 12        # Groupe 9 lit cette valeur pour générer les places
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({'erreur': str(e)}), 500
    finally:
        cur.close(); db.close()


# ─────────────────────────────────────────────────────
# GET /api/bus/<bus_id>
# Détail d'un bus — utilisé par Groupe 9
# ─────────────────────────────────────────────────────
@app.route('/api/bus/<int:bus_id>', methods=['GET'])
def detail_bus(bus_id):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT b.id, b.immatriculation, b.capacite,
               b.agence_id, a.nom AS agence_nom,
               b.trajet_id
        FROM bus b
        JOIN agences a ON a.id = b.agence_id
        WHERE b.id = %s
    """, (bus_id,))
    bus = cur.fetchone()
    cur.close(); db.close()

    if not bus:
        return jsonify({'erreur': 'Bus introuvable'}), 404
    return jsonify(bus), 200


# ─────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5008)
