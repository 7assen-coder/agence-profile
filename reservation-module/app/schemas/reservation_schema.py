from marshmallow import Schema, fields, validate


class CreerReservationSchema(Schema):
    trajet_id        = fields.Integer(required=True)
    client_nom       = fields.String(required=True, validate=validate.Length(min=2, max=120))
    client_email     = fields.Email(required=True)
    client_telephone = fields.String(load_default=None, validate=validate.Length(max=30))
    numero_place     = fields.Integer(
        required=True, validate=validate.Range(min=1, max=12)
    )


class ConfirmerReservationSchema(Schema):
    """Payload envoyé par le module Paiement pour confirmer une réservation."""
    paiement_ref = fields.String(required=True, validate=validate.Length(min=1, max=100))
