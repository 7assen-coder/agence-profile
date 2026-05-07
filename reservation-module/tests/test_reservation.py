import pytest
from app import create_app
from app.config import Config
from app.extensions import db as _db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["module"] == "gestion-reservations"


def test_creer_reservation(client):
    payload = {
        "trajet_id": 1,
        "client_nom": "Aya Diallo",
        "client_email": "aya@example.com",
        "numero_place": 5,
    }
    r = client.post("/api/reservations", json=payload)
    assert r.status_code == 201
    data = r.get_json()
    assert data["reservation"]["statut"] == "en_attente"
    assert data["reservation"]["numero_place"] == 5


def test_place_deja_prise(client):
    payload = {
        "trajet_id": 1,
        "client_nom": "Aya Diallo",
        "client_email": "aya@example.com",
        "numero_place": 3,
    }
    client.post("/api/reservations", json=payload)
    # Deuxième tentative sur la même place
    r = client.post("/api/reservations", json=payload)
    assert r.status_code == 409


def test_confirmer_reservation(client):
    payload = {
        "trajet_id": 1,
        "client_nom": "Moussa Ba",
        "client_email": "moussa@example.com",
        "numero_place": 7,
    }
    r = client.post("/api/reservations", json=payload)
    reservation_id = r.get_json()["reservation"]["id"]

    r2 = client.put(
        f"/api/reservations/{reservation_id}/confirmer",
        json={"paiement_ref": "PAY-ABC123"},
    )
    assert r2.status_code == 200
    assert r2.get_json()["reservation"]["statut"] == "confirmee"


def test_annuler_reservation(client):
    payload = {
        "trajet_id": 2,
        "client_nom": "Fatou Sow",
        "client_email": "fatou@example.com",
        "numero_place": 2,
    }
    r = client.post("/api/reservations", json=payload)
    reservation_id = r.get_json()["reservation"]["id"]

    r2 = client.delete(f"/api/reservations/{reservation_id}")
    assert r2.status_code == 200
    assert r2.get_json()["reservation"]["statut"] == "annulee"


def test_places_disponibles(client):
    payload = {
        "trajet_id": 3,
        "client_nom": "Ibra Ndiaye",
        "client_email": "ibra@example.com",
        "numero_place": 10,
    }
    client.post("/api/reservations", json=payload)

    r = client.get("/api/reservations/trajet/3/places")
    assert r.status_code == 200
    places = r.get_json()["places"]
    assert len(places) == 12
    place_10 = next(p for p in places if p["numero"] == 10)
    assert place_10["statut"] == "en_attente"
