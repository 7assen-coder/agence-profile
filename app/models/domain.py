"""Modèle domaine réservation transport (schéma MCD fourni + champs auth)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, UniqueConstraint

from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db


class Agence(db.Model):
    __tablename__ = "agences"

    id = db.Column("id_agence", db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    adresse = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    statut = db.Column(
        db.Enum(
            "active",
            "suspendue",
            "en_attente",
            name="agence_statut",
            native_enum=False,
            length=20,
        ),
        nullable=False,
        default="en_attente",
    )
    logo = db.Column(db.String(255), nullable=True)
    ville = db.Column(db.String(80), nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_maj = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    buses = db.relationship(
        "Bus", backref="agence", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "ville": self.ville,
            "description": self.description,
            "logo": self.logo,
            "statut": self.statut,
            "date_creation": self.date_creation.isoformat(),
        }

    def to_private_dict(self) -> dict:
        return {
            **self.to_public_dict(),
            "email": self.email,
            "telephone": self.telephone,
            "adresse": self.adresse,
            "role": "agence",
            "date_maj": self.date_maj.isoformat(),
        }


class Ville(db.Model):
    __tablename__ = "villes"

    id = db.Column("id_ville", db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=True)


class Bus(db.Model):
    __tablename__ = "bus"

    id = db.Column("id_bus", db.Integer, primary_key=True, autoincrement=True)
    id_agence = db.Column(
        db.Integer,
        db.ForeignKey("agences.id_agence", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    immatriculation = db.Column(db.String(20), nullable=False, unique=True)
    capacite = db.Column(db.Integer, nullable=False, default=12)

    places = db.relationship(
        "Place", backref="bus", lazy="dynamic", cascade="all, delete-orphan"
    )


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column("id_place", db.Integer, primary_key=True, autoincrement=True)
    id_bus = db.Column(
        db.Integer,
        db.ForeignKey("bus.id_bus", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    numero_place = db.Column(db.SmallInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_bus", "numero_place", name="uq_place_bus"),
        CheckConstraint(
            "numero_place >= 1 AND numero_place <= 12",
            name="chk_numero_place",
        ),
    )


class Trajet(db.Model):
    __tablename__ = "trajets"

    id = db.Column("id_trajet", db.Integer, primary_key=True, autoincrement=True)
    id_agence = db.Column(
        db.Integer,
        db.ForeignKey("agences.id_agence", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    id_bus = db.Column(
        db.Integer,
        db.ForeignKey("bus.id_bus", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    id_ville_depart = db.Column(
        db.Integer,
        db.ForeignKey("villes.id_ville", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    id_ville_arrivee = db.Column(
        db.Integer,
        db.ForeignKey("villes.id_ville", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    date_trajet = db.Column(db.Date, nullable=False)
    periode = db.Column(
        db.Enum(
            "matin",
            "apres-midi",
            name="trajet_periode",
            native_enum=False,
            length=16,
        ),
        nullable=False,
    )
    heure_depart = db.Column(db.Time, nullable=True)
    heure_arrivee = db.Column(db.Time, nullable=True)
    prix = db.Column(db.Numeric(10, 2), nullable=False)


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column("id_client", db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    cin = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Administrateur(db.Model):
    __tablename__ = "administrateurs"

    id = db.Column("id_admin", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(100), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Paiement(db.Model):
    __tablename__ = "paiements"

    id = db.Column("id_paiement", db.Integer, primary_key=True, autoincrement=True)
    id_client = db.Column(
        db.Integer,
        db.ForeignKey("clients.id_client", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    montant = db.Column(db.Numeric(10, 2), nullable=False)
    date_paiement = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    mode_paiement = db.Column(
        db.Enum(
            "especes",
            "carte",
            "mobile_money",
            "virement",
            name="paiement_mode",
            native_enum=False,
            length=20,
        ),
        nullable=False,
    )
    statut = db.Column(
        db.Enum(
            "en_attente",
            "confirme",
            "echoue",
            "rembourse",
            name="paiement_statut",
            native_enum=False,
            length=20,
        ),
        nullable=False,
        default="en_attente",
    )


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column("id_reservation", db.Integer, primary_key=True, autoincrement=True)
    id_client = db.Column(
        db.Integer,
        db.ForeignKey("clients.id_client", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    id_place = db.Column(
        db.Integer,
        db.ForeignKey("places.id_place", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    id_trajet = db.Column(
        db.Integer,
        db.ForeignKey("trajets.id_trajet", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    id_paiement = db.Column(
        db.Integer,
        db.ForeignKey("paiements.id_paiement", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    date_reservation = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    statut = db.Column(
        db.Enum(
            "en_attente",
            "confirmee",
            "annulee",
            name="reservation_statut",
            native_enum=False,
            length=20,
        ),
        nullable=False,
        default="en_attente",
    )

    __table_args__ = (
        UniqueConstraint("id_place", "id_trajet", name="uq_place_trajet_active"),
    )
