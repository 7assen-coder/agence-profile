"""Comptes de démonstration (idempotent)."""
from __future__ import annotations

from app.extensions import db
from app.models import Administrateur, Agence, Client, Ville

# Identifiants à communiquer à l’équipe (démo locale)
DEMO_CLIENT_EMAIL = "client.demo@transport.ma"
DEMO_CLIENT_PASSWORD = "ClientDemo2026!"

DEMO_AGENCE_EMAIL = "agence.demo@transport.ma"
DEMO_AGENCE_PASSWORD = "AgenceDemo2026!"

DEMO_ADMIN_EMAIL = "admin@transport.ma"
DEMO_ADMIN_PASSWORD = "AdminDemo2026!"


def seed_demo_users() -> None:
    if not Client.query.filter_by(email=DEMO_CLIENT_EMAIL).first():
        c = Client(
            nom="Benani",
            prenom="Samira",
            telephone="24123456",
            email=DEMO_CLIENT_EMAIL,
            cin="1234567890",
        )
        c.set_password(DEMO_CLIENT_PASSWORD)
        db.session.add(c)

    if not Agence.query.filter_by(email=DEMO_AGENCE_EMAIL).first():
        a = Agence(
            nom="Agence Démo Nord",
            telephone="32199887",
            email=DEMO_AGENCE_EMAIL,
            adresse="Avenue Kennedy, Nouakchott",
            statut="active",
            ville="Nouakchott",
            description="Compte agence de démonstration.",
        )
        a.set_password(DEMO_AGENCE_PASSWORD)
        db.session.add(a)

    if not Administrateur.query.filter_by(email=DEMO_ADMIN_EMAIL).first():
        ad = Administrateur(
            nom="Super Admin",
            email=DEMO_ADMIN_EMAIL,
        )
        ad.set_password(DEMO_ADMIN_PASSWORD)
        db.session.add(ad)

    if Ville.query.count() == 0:
        db.session.add_all(
            [
                Ville(nom="Nouakchott", region="Trarza"),
                Ville(nom="Nouadhibou", region="Dakhlet Nouadhibou"),
                Ville(nom="Rosso", region="Trarza"),
            ]
        )

    db.session.commit()
