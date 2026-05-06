from flask import Blueprint, jsonify, request
from .models import (
    generer_places,
    get_places_par_bus,
    get_places_par_trajet,
    supprimer_places,
    get_all_bus,
)

places_bp = Blueprint("api_places", __name__)


# ── POST /api/places/generer ────────────────────────────────────────────────
@places_bp.post("/generer")
def route_generer():
    """
    Body JSON : { "id_bus": 3, "capacite": 15 }
    capacite est optionnel : si absent, on utilise la valeur de la table bus.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"erreur": "Corps JSON manquant."}), 400

    id_bus = data.get("id_bus")
    capacite = data.get("capacite")  # optionnel

    if id_bus is None:
        return jsonify({"erreur": "Champ requis : id_bus."}), 400
    if not isinstance(id_bus, int) or id_bus <= 0:
        return jsonify({"erreur": "id_bus doit être un entier positif."}), 400
    if capacite is not None and not isinstance(capacite, int):
        return jsonify({"erreur": "capacite doit être un entier."}), 400

    try:
        resultat = generer_places(id_bus, capacite)
        return jsonify(resultat), 201
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 422
    except RuntimeError as e:
        return jsonify({"erreur": str(e)}), 409
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500


# ── GET /api/places/<id_bus> ────────────────────────────────────────────────
@places_bp.get("/<int:id_bus>")
def route_get_places(id_bus):
    trajet_id = request.args.get("trajet_id", type=int)
    try:
        if trajet_id:
            places = get_places_par_trajet(id_bus, trajet_id)
        else:
            places = get_places_par_bus(id_bus)

        if not places:
            return jsonify({"erreur": f"Aucune place trouvée pour le bus {id_bus}."}), 404

        return jsonify({
            "id_bus": id_bus,
            "trajet_id": trajet_id,
            "total": len(places),
            "places": places,
        }), 200
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500


# ── DELETE /api/places/<id_bus> ─────────────────────────────────────────────
@places_bp.delete("/<int:id_bus>")
def route_supprimer(id_bus):
    try:
        return jsonify(supprimer_places(id_bus)), 200
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500


# ── GET /api/places/bus ─────────────────────────────────────────────────────
@places_bp.get("/bus")
def route_all_bus():
    try:
        return jsonify(get_all_bus()), 200
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500
