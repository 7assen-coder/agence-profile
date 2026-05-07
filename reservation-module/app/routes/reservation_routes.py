from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError

from ..extensions import db
from ..models.reservation import Reservation
from ..schemas.reservation_schema import CreerReservationSchema, ConfirmerReservationSchema

reservation_bp = Blueprint("reservations", __name__)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _liberer_places_expirees(trajet_id: int) -> None:
    """Libère automatiquement les places dont le blocage temporaire a expiré."""
    expirees = Reservation.query.filter(
        Reservation.trajet_id == trajet_id,
        Reservation.statut == "en_attente",
        Reservation.date_expiration < datetime.utcnow(),
    ).all()
    for r in expirees:
        r.statut = "annulee"
    if expirees:
        db.session.commit()


# ── POST /api/reservations ────────────────────────────────────────────────────

@reservation_bp.post("")
def creer_reservation():
    """
    Crée une réservation et bloque la place temporairement (15 min).
    Le module Paiement doit confirmer avant l'expiration.
    """
    try:
        data = CreerReservationSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(error="validation_error", details=err.messages), 400

    trajet_id    = data["trajet_id"]
    numero_place = data["numero_place"]

    # Libère d'abord les places expirées pour ce trajet
    _liberer_places_expirees(trajet_id)

    # Vérifie si la place est déjà prise (en_attente ou confirmee)
    place_prise = Reservation.query.filter(
        Reservation.trajet_id    == trajet_id,
        Reservation.numero_place == numero_place,
        Reservation.statut.in_(["en_attente", "confirmee"]),
    ).first()

    if place_prise:
        return jsonify(error="place_non_disponible",
                       message=f"La place {numero_place} est déjà réservée."), 409

    expiration_minutes = current_app.config.get("RESERVATION_EXPIRATION_MINUTES", 15)
    reservation = Reservation(
        trajet_id        = trajet_id,
        client_nom       = data["client_nom"],
        client_email     = data["client_email"],
        client_telephone = data.get("client_telephone"),
        numero_place     = numero_place,
        statut           = "en_attente",
        date_expiration  = datetime.utcnow() + timedelta(minutes=expiration_minutes),
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify(
        message="place_bloquee",
        reservation=reservation.to_dict(),
        expiration_minutes=expiration_minutes,
    ), 201


# ── GET /api/reservations/<id> ────────────────────────────────────────────────

@reservation_bp.get("/<int:reservation_id>")
def get_reservation(reservation_id):
    """Retourne les détails d'une réservation."""
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify(error="reservation_introuvable"), 404

    # Marque automatiquement comme annulée si expirée
    if reservation.is_expiree():
        reservation.statut = "annulee"
        db.session.commit()

    return jsonify(reservation=reservation.to_dict())


# ── PUT /api/reservations/<id>/confirmer ─────────────────────────────────────

@reservation_bp.put("/<int:reservation_id>/confirmer")
def confirmer_reservation(reservation_id):
    """
    Confirme la réservation après paiement réussi.
    Appelé par le module Paiement.
    """
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify(error="reservation_introuvable"), 404

    if reservation.statut == "confirmee":
        return jsonify(error="deja_confirmee"), 400

    if reservation.statut == "annulee":
        return jsonify(error="reservation_annulee"), 400

    if reservation.is_expiree():
        reservation.statut = "annulee"
        db.session.commit()
        return jsonify(error="reservation_expiree",
                       message="Le délai de paiement est dépassé, la place a été libérée."), 410

    try:
        data = ConfirmerReservationSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(error="validation_error", details=err.messages), 400

    reservation.statut          = "confirmee"
    reservation.date_expiration = None   # plus besoin du blocage
    db.session.commit()

    return jsonify(
        message="reservation_confirmee",
        reservation=reservation.to_dict(),
        paiement_ref=data["paiement_ref"],
    )


# ── DELETE /api/reservations/<id> ────────────────────────────────────────────

@reservation_bp.delete("/<int:reservation_id>")
def annuler_reservation(reservation_id):
    """Annule une réservation et libère la place."""
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify(error="reservation_introuvable"), 404

    if reservation.statut == "confirmee":
        return jsonify(error="impossible_annuler_confirmee",
                       message="Une réservation confirmée ne peut pas être annulée ici."), 400

    reservation.statut = "annulee"
    db.session.commit()

    return jsonify(message="reservation_annulee", reservation=reservation.to_dict())


# ── GET /api/reservations/trajet/<trajet_id>/places ──────────────────────────

@reservation_bp.get("/trajet/<int:trajet_id>/places")
def places_disponibles(trajet_id):
    """
    Retourne les 12 places du trajet avec leur disponibilité en temps réel.
    """
    _liberer_places_expirees(trajet_id)

    reservees = Reservation.query.filter(
        Reservation.trajet_id == trajet_id,
        Reservation.statut.in_(["en_attente", "confirmee"]),
    ).all()

    places_prises = {r.numero_place: r.statut for r in reservees}

    places = []
    for num in range(1, 13):
        statut = places_prises.get(num, "disponible")
        places.append({"numero": num, "statut": statut})

    return jsonify(trajet_id=trajet_id, places=places)


# ── GET /api/reservations (admin) ─────────────────────────────────────────────

@reservation_bp.get("")
def lister_reservations():
    """Liste toutes les réservations (vue admin)."""
    statut    = request.args.get("statut")
    trajet_id = request.args.get("trajet_id", type=int)

    query = Reservation.query
    if statut:
        query = query.filter_by(statut=statut)
    if trajet_id:
        query = query.filter_by(trajet_id=trajet_id)

    reservations = query.order_by(Reservation.date_creation.desc()).all()
    return jsonify(
        total=len(reservations),
        items=[r.to_dict() for r in reservations],
    )
