"""
Tests minimaux — utilisent SQLite en mémoire.
Lancer: pytest -q
"""
import pytest
from app import create_app
from app.extensions import db
from app.config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    JWT_SECRET_KEY = "test-jwt"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_register_and_login(client):
    r = client.post("/api/auth/register", json={
        "nom": "Agence Test",
        "email": "test@agence.ma",
        "password": "motdepasse123",
        "ville": "Nouakchott",
    })
    assert r.status_code == 201

    r = client.post("/api/auth/login", json={
        "email": "test@agence.ma",
        "password": "motdepasse123",
    })
    assert r.status_code == 200
    assert "access_token" in r.get_json()


def test_update_profile(client):
    client.post("/api/auth/register", json={
        "nom": "Agence A",
        "email": "a@a.ma",
        "password": "motdepasse123",
    })
    token = client.post("/api/auth/login", json={
        "email": "a@a.ma", "password": "motdepasse123",
    }).get_json()["access_token"]

    r = client.put(
        "/api/agences/me",
        json={"ville": "Rosso"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.get_json()["agence"]["ville"] == "Rosso"
