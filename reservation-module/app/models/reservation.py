from datetime import datetime
from ..extensions import db


class Reservation(db.Model):
    __tablename__ = "reservations"

    id               = db.Column(db.Integer, primary_key=True)
    trajet_id        = db.Column(db.Integer, nullable=False, index=True)
    client_nom       = db.Column(db.String(120), nullable=False)
    client_email     = db.Column(db.String(120), nullable=False, index=True)
    client_telephone = db.Column(db.String(30), nullable=True)
    numero_place     = db.Column(db.Integer, nullable=False)
    statut           = db.Column(
        db.Enum("en_attente", "confirmee", "annulee", name="reservation_statut"),
        nullable=False,
        default="en_attente",
    )
    date_expiration  = db.Column(db.DateTime, nullable=True)   # blocage 15 min
    date_creation    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_maj         = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def is_expiree(self) -> bool:
        """Vérifie si le blocage temporaire a expiré."""
        if self.statut == "en_attente" and self.date_expiration:
            return datetime.utcnow() > self.date_expiration
        return False

    def to_dict(self) -> dict:
        return {
            "id":               self.id,
            "trajet_id":        self.trajet_id,
            "client_nom":       self.client_nom,
            "client_email":     self.client_email,
            "client_telephone": self.client_telephone,
            "numero_place":     self.numero_place,
            "statut":           self.statut,
            "date_expiration":  self.date_expiration.isoformat() if self.date_expiration else None,
            "date_creation":    self.date_creation.isoformat(),
            "date_maj":         self.date_maj.isoformat(),
        }
