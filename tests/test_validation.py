from app.schemas.validation_schemas import (
    validate_agence_data,
    validate_trajet_data,
    validate_place_data,
    validate_paiement_data,
    validate_bus_data,
    validate_client_data,
    validate_promotion_data,
    validate_disponibilite_data
)


def test_agence_email_invalide():
    data = {
        "nom": "Agence Test",
        "email": "email_invalide",
        "telephone": "22200000"
    }

    errors = validate_agence_data(data)

    assert "email" in errors


def test_trajet_villes_identiques():
    data = {
        "ville_depart_id": 1,
        "ville_arrivee_id": 1,
        "horaire": "matin",
        "prix": 500,
        "distance": 100,
        "date_depart": "2026-05-06"
    }

    errors = validate_trajet_data(data)

    assert "ville_arrivee_id" in errors


def test_place_numero_invalide():
    data = {
        "numero": 15,
        "trajet_id": 1
    }

    errors = validate_place_data(data)

    assert "numero" in errors


def test_paiement_montant_negatif():
    data = {
        "reservation_id": 1,
        "montant": -500,
        "mode_paiement": "bankily"
    }

    errors = validate_paiement_data(data)

    assert "montant" in errors


def test_bus_capacite_invalide():
    data = {
        "trajet_id": 1,
        "capacite": 20
    }

    errors = validate_bus_data(data)

    assert "capacite" in errors


def test_client_mot_de_passe_court():
    data = {
        "nom": "Client Test",
        "email": "client@test.com",
        "telephone": "22200000",
        "mot_de_passe": "123"
    }

    errors = validate_client_data(data)

    assert "mot_de_passe" in errors


def test_promotion_valeur_invalide():
    data = {
        "code": "PROMO10",
        "valeur": -10
    }

    errors = validate_promotion_data(data)

    assert "valeur" in errors


def test_disponibilite_place_invalide():
    data = {
        "trajet_id": 1,
        "numero_place": 20
    }

    errors = validate_disponibilite_data(data)

    assert "numero_place" in errors