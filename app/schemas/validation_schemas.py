from app.utils.validators import (
    is_required,
    is_valid_email,
    is_valid_phone,
    is_positive_number,
    is_valid_place_number,
    is_valid_horaire,
    is_valid_status_reservation,
)

def validate_agence_data(data):
    errors = {}

    if not is_required(data.get("nom")):
        errors["nom"] = "Le nom de l'agence est obligatoire."

    if not is_valid_email(data.get("email")):
        errors["email"] = "Adresse email invalide."

    if not is_valid_phone(data.get("telephone")):
        errors["telephone"] = "Numéro de téléphone invalide."

    return errors


def validate_client_data(data):
    errors = {}

    if not is_required(data.get("nom")):
        errors["nom"] = "Le nom du client est obligatoire."

    if not is_valid_email(data.get("email")):
        errors["email"] = "Adresse email invalide."

    if not is_valid_phone(data.get("telephone")):
        errors["telephone"] = "Numéro de téléphone invalide."

    if not is_required(data.get("mot_de_passe")) or len(data.get("mot_de_passe", "")) < 6:
        errors["mot_de_passe"] = "Le mot de passe doit contenir au moins 6 caractères."

    return errors


def validate_trajet_data(data):
    errors = {}

    if not is_required(data.get("ville_depart_id")):
        errors["ville_depart_id"] = "La ville de départ est obligatoire."

    if not is_required(data.get("ville_arrivee_id")):
        errors["ville_arrivee_id"] = "La ville d'arrivée est obligatoire."

    if data.get("ville_depart_id") == data.get("ville_arrivee_id"):
        errors["ville_arrivee_id"] = "La ville d'arrivée doit être différente de la ville de départ."

    if not is_valid_horaire(data.get("horaire")):
        errors["horaire"] = "L'horaire doit être 'matin' ou 'apres_midi'."

    if not is_positive_number(data.get("prix")):
        errors["prix"] = "Le prix doit être positif."

    if not is_positive_number(data.get("distance")):
        errors["distance"] = "La distance doit être positive."

    return errors


def validate_place_data(data):
    errors = {}

    if not is_valid_place_number(data.get("numero")):
        errors["numero"] = "Le numéro de place doit être compris entre 1 et 12."

    if not is_required(data.get("trajet_id")):
        errors["trajet_id"] = "Le trajet est obligatoire."

    return errors


def validate_reservation_data(data):
    errors = {}

    if not is_required(data.get("client_id")):
        errors["client_id"] = "Le client est obligatoire."

    if not is_required(data.get("place_id")):
        errors["place_id"] = "La place est obligatoire."

    status = data.get("statut", "en_attente")
    if not is_valid_status_reservation(status):
        errors["statut"] = "Statut invalide."

    return errors


def validate_paiement_data(data):
    errors = {}

    if not is_required(data.get("reservation_id")):
        errors["reservation_id"] = "La réservation est obligatoire."

    if not is_positive_number(data.get("montant")):
        errors["montant"] = "Le montant doit être positif."

    return errors