from flask import Blueprint, jsonify, request
from .models import generer_places, get_places_par_bus, supprimer_places

places_bp = Blueprint("places", __name__)


@places_bp.post("/generer")
def route_generer():
    """
    POST /places/generer
    Body JSON : { "id_bus": 3, "capacite": 15 }

    Génère les places numérotées 1..capacite pour le bus.
    Appelé par l'équipe 'gestion des bus' après création d'un bus.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"erreur": "Corps JSON manquant."}), 400

    id_bus = data.get("id_bus")
    capacite = data.get("capacite")

    if id_bus is None or capacite is None:
        return jsonify({"erreur": "Champs requis : id_bus, capacite."}), 400

    if not isinstance(id_bus, int) or id_bus <= 0:
        return jsonify({"erreur": "id_bus doit être un entier positif."}), 400

    if not isinstance(capacite, int):
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


@places_bp.get("/<int:id_bus>")
def route_get_places(id_bus):
    """
    GET /places/<id_bus>

    Retourne la liste des places d'un bus.
    Utilisé par l'équipe affichage.
    """
    try:
        places = get_places_par_bus(id_bus)
        if not places:
            return jsonify({"erreur": f"Aucune place trouvée pour le bus {id_bus}."}), 404
        return jsonify({"id_bus": id_bus, "total": len(places), "places": places}), 200
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500


@places_bp.delete("/<int:id_bus>")
def route_supprimer(id_bus):
    """
    DELETE /places/<id_bus>

    Supprime toutes les places d'un bus (reconfiguration).
    """
    try:
        resultat = supprimer_places(id_bus)
        return jsonify(resultat), 200
    except Exception as e:
        return jsonify({"erreur": "Erreur interne.", "detail": str(e)}), 500
