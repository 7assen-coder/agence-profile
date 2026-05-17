from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from ..extensions import db
from ..models.agence import Agence
from ..schemas.agence_schema import (
    UpdateProfileSchema,
    ChangePasswordSchema,
    AdminUpdateStatutSchema,
)
from ..utils.auth import role_required, current_agence
from ..utils.validators import allowed_file, save_logo

agence_bp = Blueprint("agences", __name__)


@agence_bp.get("/me")
@jwt_required()
def get_me():
    agence = current_agence()
    if not agence:
        return jsonify(error="agence_introuvable"), 404
    return jsonify(agence=agence.to_private_dict())


@agence_bp.put("/me")
@jwt_required()
def update_me():
    agence = current_agence()
    if not agence:
        return jsonify(error="agence_introuvable"), 404

    try:
        data = UpdateProfileSchema().load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify(error="validation_error", details=err.messages), 400

    for field, value in data.items():
        setattr(agence, field, value)

    db.session.commit()
    return jsonify(message="profil_mis_a_jour", agence=agence.to_private_dict())


@agence_bp.put("/me/password")
@jwt_required()
def change_password():
    agence = current_agence()
    if not agence:
        return jsonify(error="agence_introuvable"), 404

    payload = request.get_json() or {}
    schema = ChangePasswordSchema()
    schema.context = {"ancien_password": payload.get("ancien_password")}

    try:
        data = schema.load(payload)
    except ValidationError as err:
        return jsonify(error="validation_error", details=err.messages), 400

    if not agence.check_password(data["ancien_password"]):
        return jsonify(error="ancien_password_incorrect"), 400

    agence.set_password(data["nouveau_password"])
    db.session.commit()
    return jsonify(message="mot_de_passe_change")


@agence_bp.post("/me/logo")
@jwt_required()
def upload_logo():
    agence = current_agence()
    if not agence:
        return jsonify(error="agence_introuvable"), 404

    if "logo" not in request.files:
        return jsonify(error="fichier_manquant"), 400

    file = request.files["logo"]
    if file.filename == "":
        return jsonify(error="fichier_vide"), 400
    if not allowed_file(file.filename):
        return jsonify(error="extension_non_autorisee"), 400

    filename = save_logo(file)
    agence.logo = filename
    db.session.commit()
    return jsonify(message="logo_televerse", logo=filename)


@agence_bp.get("/logos/<path:filename>")
def serve_logo(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@agence_bp.delete("/me")
@jwt_required()
def delete_me():
    agence = current_agence()
    if not agence:
        return jsonify(error="agence_introuvable"), 404
    db.session.delete(agence)
    db.session.commit()
    return jsonify(message="compte_supprime")


# ---------------- Routes publiques ----------------

@agence_bp.get("")
def list_agences():
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    ville = request.args.get("ville")

    query = Agence.query.filter_by(statut="active")
    if ville:
        query = query.filter(Agence.ville.ilike(f"%{ville}%"))

    pagination = query.order_by(Agence.nom.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify(
        items=[a.to_public_dict() for a in pagination.items],
        total=pagination.total,
        page=pagination.page,
        pages=pagination.pages,
    )


@agence_bp.get("/<int:agence_id>")
def get_agence_public(agence_id):
    agence = Agence.query.get(agence_id)
    if not agence or agence.statut != "active":
        return jsonify(error="agence_introuvable"), 404
    return jsonify(agence=agence.to_public_dict())


# ---------------- Routes admin ----------------

@agence_bp.get("/admin/all")
@role_required("admin")
def admin_list():
    agences = Agence.query.order_by(Agence.date_creation.desc()).all()
    return jsonify(items=[a.to_private_dict() for a in agences])


@agence_bp.put("/admin/<int:agence_id>/statut")
@role_required("admin")
def admin_update_statut(agence_id):
    agence = Agence.query.get(agence_id)
    if not agence:
        return jsonify(error="agence_introuvable"), 404

    try:
        data = AdminUpdateStatutSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(error="validation_error", details=err.messages), 400

    agence.statut = data["statut"]
    db.session.commit()
    return jsonify(message="statut_mis_a_jour", agence=agence.to_private_dict())
