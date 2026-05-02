from flask import Blueprint, jsonify, request
from .models import generer_places, get_places_par_bus, supprimer_places

places_bp = Blueprint("places", __name__)


@places_bp.post("/generer")
def route_generer():
    """
    POST /places/generer
    Body JSON : { "bus_id": 3, "capacite": 15 }

    Génère les places numérotées 1..capacite pour le bus.
    Appelé par l'équipe 'gestion des bus' après création d'un bus.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"erreur": "Corps JSON manquant."}), 400

    bus_id = data.get("bus_id")
    capacite = data.get("capacite")

    if bus_id is None or capacite is None:
        return jsonify({"erreur": "Champs requis : bus_id, capacite."}), 400

    if not isinstance(bus_id, int) or bus_id <= 0:
        return jsonify({"erreur": "bus_id doit être un entier positif."}), 400

    if not isinstance(capacite, int):
        return jsonify({"erreur": "capacite doit être un entier."}), 400

    try:
        resultat = generer_places(bus_id, capacite)
        return jsonify(resultat), 201
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 422
    except RuntimeError as e:
        return jsonify({"erreur": str(e)}), 409
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500


@places_bp.get("/<int:bus_id>")
def route_get_places(bus_id):
    """
    GET /places/<bus_id>

    Retourne la liste des places d'un bus.
    Utilisé par l'équipe affichage.
    """
    try:
        places = get_places_par_bus(bus_id)
        if not places:
            return jsonify({"erreur": f"Aucune place trouvée pour le bus {bus_id}."}), 404
        return jsonify({"bus_id": bus_id, "total": len(places), "places": places}), 200
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500


@places_bp.delete("/<int:bus_id>")
def route_supprimer(bus_id):
    """
    DELETE /places/<bus_id>

    Supprime toutes les places d'un bus (reconfiguration).
    """
    try:
        resultat = supprimer_places(bus_id)
        return jsonify(resultat), 200
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500
