from flask import Blueprint, request, jsonify, render_template
from app.services.trajets_service import (
    lister_villes,
    rechercher_trajets,
    detail_trajet
)

bp = Blueprint("recherche", __name__)

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/api/villes", methods=["GET"])
def villes():
    try:
        resultats = lister_villes()
        return jsonify({"success": True, "villes": resultats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route("/api/trajets/recherche", methods=["GET"])
def recherche():
    try:
        resultats = rechercher_trajets(
            ville_depart  = request.args.get("ville_depart"),
            ville_arrivee = request.args.get("ville_arrivee"),
            date          = request.args.get("date"),
            periode       = request.args.get("periode"),
            agence        = request.args.get("agence"),
            prix_max      = request.args.get("prix_max", type=float),
            tri           = request.args.get("tri", "heure_depart")
        )
        return jsonify({"success": True, "count": len(resultats), "trajets": resultats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route("/api/trajets/<int:id_trajet>", methods=["GET"])
def details(id_trajet):
    try:
        trajet = detail_trajet(id_trajet)
        if not trajet:
            return jsonify({"success": False, "error": "Trajet introuvable"}), 404
        return jsonify({"success": True, "trajet": trajet}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
