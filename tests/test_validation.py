from app.schemas.validation_schemas import (
    validate_agence_data,
    validate_trajet_data,
    validate_place_data,
)

def test_agence_email_invalide():
    data = {
        "nom": "Agence Test",
        "email": "email_faux",
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
        "distance": 100
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