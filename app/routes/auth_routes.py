from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models.agence import Agence
from ..schemas.agence_schema import RegisterSchema, LoginSchema

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    try:
        data = RegisterSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(error="validation_error", details=err.messages), 400

    if Agence.query.filter_by(email=data["email"]).first():
        return jsonify(error="email_already_used"), 409

    agence = Agence(
        nom=data["nom"],
        email=data["email"],
        telephone=data.get("telephone"),
        adresse=data.get("adresse"),
        ville=data.get("ville"),
        description=data.get("description"),
        statut="en_attente",
        role="agence",
    )
    agence.set_password(data["password"])

    try:
        db.session.add(agence)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="email_already_used"), 409

    return (
        jsonify(
            message="agence_enregistree",
            agence=agence.to_private_dict(),
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    try:
        data = LoginSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(error="validation_error", details=err.messages), 400

    agence = Agence.query.filter_by(email=data["email"]).first()
    if not agence or not agence.check_password(data["password"]):
        return jsonify(error="identifiants_invalides"), 401

    if agence.statut == "suspendue":
        return jsonify(error="compte_suspendu"), 403

    token = create_access_token(
        identity=str(agence.id),
        additional_claims={"role": agence.role, "email": agence.email},
    )
    return jsonify(
        access_token=token,
        token_type="Bearer",
        agence=agence.to_private_dict(),
    )
