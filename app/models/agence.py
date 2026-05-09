from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db


class Agence(db.Model):
    __tablename__ = "agences"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(30), nullable=True)
    adresse = db.Column(db.String(255), nullable=True)
    ville = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    statut = db.Column(
        db.Enum("active", "suspendue", "en_attente", name="agence_statut"),
        nullable=False,
        default="en_attente",
    )
    role = db.Column(
        db.Enum("agence", "admin", name="agence_role"),
        nullable=False,
        default="agence",
    )
    date_creation = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_maj = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
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
            "role": self.role,
            "date_maj": self.date_maj.isoformat(),
        }
