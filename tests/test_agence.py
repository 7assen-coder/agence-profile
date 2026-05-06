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
        "email": "contact@gmail.com",
        "password": "motdepasse123",
    })
    token = client.post("/api/auth/login", json={
        "email": "contact@gmail.com", "password": "motdepasse123",
    }).get_json()["access_token"]

    r = client.put(
        "/api/agences/me",
        json={"ville": "Rosso"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.get_json()["agence"]["ville"] == "Rosso"


def test_web_home(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Bienvenue" in r.get_data(as_text=True)


def test_web_agences_requires_login(client):
    r = client.get("/agences", follow_redirects=False)
    assert r.status_code == 302
    assert "/" in r.location and "next=" in r.location and "agences" in r.location


def test_api_agences_requires_auth(client):
    r = client.get("/api/agences")
    assert r.status_code == 401


def test_api_agences_ok_with_jwt(client):
    client.post("/api/auth/register", json={
        "nom": "Jwt Liste",
        "email": "jwtl@agence.ma",
        "password": "motdepasse12345",
        "ville": "Ndb",
    })
    tok = client.post("/api/auth/login", json={
        "email": "jwtl@agence.ma",
        "password": "motdepasse12345",
    }).get_json()["access_token"]
    r = client.get("/api/agences", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200


def test_web_agences_with_session(app, client):
    from app.models import Client
    from app.utils.session_auth import KIND_CLIENT, SESSION_ID, SESSION_KIND

    with app.app_context():
        c = Client(
            nom="L",
            prenom="Ann",
            email="ann@gmail.com",
            cin="8877665544",
        )
        c.set_password("motdepasse123456")
        db.session.add(c)
        db.session.commit()
        cid = c.id
    with client.session_transaction() as sess:
        sess[SESSION_KIND] = KIND_CLIENT
        sess[SESSION_ID] = cid
    r = client.get("/agences")
    assert r.status_code == 200
    assert "Agences actives" in r.get_data(as_text=True)
