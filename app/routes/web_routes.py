from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)

from ..extensions import db
from ..models import Administrateur, Agence, Client, Bus, Reservation, Trajet
from ..schemas.agence_schema import (
    UpdateProfileSchema,
    ChangePasswordSchema,
    RegisterSchema,
)
from ..utils.session_auth import (
    KIND_ADMIN,
    KIND_AGENCE,
    KIND_CLIENT,
    get_session_admin,
    get_session_agence,
    get_session_client,
    login_required_web,
    login_session,
    logout_session,
    require_session_kind,
    safe_redirect_target,
    session_kind,
)
from ..utils.input_regex import (
    is_val_err,
    validate_adresse_optional,
    validate_agence_nom,
    validate_cin,
    validate_description_optional,
    validate_email,
    validate_name_person,
    validate_password,
    validate_phone_optional,
    validate_ville_optional,
)
from ..utils.validators import allowed_file, save_logo

web_bp = Blueprint("web", __name__)


def _redirect_espace():
    k = session_kind()
    if k == KIND_CLIENT:
        return redirect(url_for("web.espace_client"))
    if k == KIND_AGENCE:
        return redirect(url_for("web.espace_agence"))
    if k == KIND_ADMIN:
        return redirect(url_for("web.espace_admin"))
    return redirect(url_for("web.home"))


# --------------------------------------------------------------------------- #
# Accueil (hub)
# --------------------------------------------------------------------------- #
@web_bp.route("/")
def home():
    if session_kind():
        return _redirect_espace()
    return render_template(
        "hub.html",
        active_nav="home",
        next_param=request.args.get("next") or None,
    )


# --------------------------------------------------------------------------- #
# Connexion par rôle
# --------------------------------------------------------------------------- #
@web_bp.route("/connexion/<role>", methods=["GET", "POST"])
def connexion_role(role):
    role = (role or "").lower().strip()
    if role not in ("client", "agence", "admin"):
        flash("Rôle inconnu.", "error")
        return redirect(url_for("web.home"))

    if session_kind():
        return _redirect_espace()

    next_target = request.args.get("next") if request.method == "GET" else None
    if request.method == "POST":
        next_target = request.form.get("next") or request.args.get("next")

    if request.method == "POST":
        email_r = validate_email(request.form.get("email", ""))
        pwd = request.form.get("password", "")
        if is_val_err(email_r):
            flash(email_r["_error"], "error")
            return (
                render_template(
                    f"connexion_{role}.html",
                    active_nav="auth",
                    next_param=next_target,
                ),
                400,
            )
        if is_val_err(validate_password(pwd)):
            flash("Mot de passe invalide.", "error")
            return (
                render_template(
                    f"connexion_{role}.html",
                    active_nav="auth",
                    next_param=next_target,
                ),
                400,
            )

        if role == "client":
            u = Client.query.filter_by(email=email_r).first()
            if not u or not u.check_password(pwd):
                flash("Email ou mot de passe incorrect.", "error")
                return (
                    render_template(
                        "connexion_client.html",
                        active_nav="auth",
                        next_param=next_target,
                    ),
                    401,
                )
            login_session(KIND_CLIENT, u.id)
        elif role == "agence":
            u = Agence.query.filter_by(email=email_r).first()
            if not u or not u.check_password(pwd):
                flash("Email ou mot de passe incorrect.", "error")
                return (
                    render_template(
                        "connexion_agence.html",
                        active_nav="auth",
                        next_param=next_target,
                    ),
                    401,
                )
            if u.statut == "suspendue":
                flash("Compte suspendu.", "error")
                return (
                    render_template(
                        "connexion_agence.html",
                        active_nav="auth",
                        next_param=next_target,
                    ),
                    403,
                )
            login_session(KIND_AGENCE, u.id)
        else:
            u = Administrateur.query.filter_by(email=email_r).first()
            if not u or not u.check_password(pwd):
                flash("Email ou mot de passe incorrect.", "error")
                return (
                    render_template(
                        "connexion_admin.html",
                        active_nav="auth",
                        next_param=next_target,
                    ),
                    401,
                )
            login_session(KIND_ADMIN, u.id)

        dest = (
            safe_redirect_target(next_target, "web.espace_" + role)
            if role != "admin"
            else safe_redirect_target(next_target, "web.espace_admin")
        )
        return redirect(dest)

    return render_template(
        f"connexion_{role}.html",
        active_nav="auth",
        next_param=next_target,
    )


# --------------------------------------------------------------------------- #
# Inscription (pas d’admin)
# --------------------------------------------------------------------------- #
@web_bp.route("/inscription/<role>", methods=["GET", "POST"])
def inscription_role(role):
    role = (role or "").lower().strip()
    if role not in ("client", "agence"):
        flash("Inscription non disponible pour ce profil.", "error")
        return redirect(url_for("web.home"))

    if session_kind():
        return _redirect_espace()

    old = {}

    if request.method == "POST":
        old = dict(request.form)

        if role == "client":
            nom = validate_name_person(request.form.get("nom", ""), "Nom")
            prenom = validate_name_person(
                request.form.get("prenom", ""), "Prénom"
            )
            email_f = validate_email(request.form.get("email", ""))
            tel = validate_phone_optional(request.form.get("telephone"))
            cin = validate_cin(request.form.get("cin", ""))
            pwd = validate_password(request.form.get("password", ""))

            for v in (nom, prenom, email_f, tel, cin, pwd):
                if is_val_err(v):
                    flash(v["_error"], "error")
                    return (
                        render_template(
                            "inscription_client.html",
                            active_nav="auth",
                            old=old,
                        ),
                        400,
                    )

            cl = Client(
                nom=nom,
                prenom=prenom,
                email=email_f,
                telephone=tel,
                cin=cin,
            )
            cl.set_password(pwd)
            try:
                db.session.add(cl)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("Email ou CIN déjà utilisé.", "error")
                return (
                    render_template(
                        "inscription_client.html",
                        active_nav="auth",
                        old=old,
                    ),
                    409,
                )
            login_session(KIND_CLIENT, cl.id)
            flash("Compte client créé.", "success")
            return redirect(url_for("web.espace_client"))

        payload = {
            "nom": request.form.get("nom", ""),
            "email": request.form.get("email", ""),
            "password": request.form.get("password", ""),
            "telephone": request.form.get("telephone") or None,
            "adresse": request.form.get("adresse") or None,
            "ville": request.form.get("ville") or None,
            "description": request.form.get("description") or None,
        }
        try:
            data = RegisterSchema().load(payload)
        except ValidationError as e:
            flash(" · ".join(f"{k}: {v}" for k, v in e.messages.items()), "error")
            return (
                render_template(
                    "inscription_agence.html",
                    active_nav="auth",
                    old=old,
                ),
                400,
            )

        extra_nom = validate_agence_nom(data["nom"])
        if is_val_err(extra_nom):
            flash(extra_nom["_error"], "error")
            return (
                render_template(
                    "inscription_agence.html",
                    active_nav="auth",
                    old=old,
                ),
                400,
            )
        ad = validate_adresse_optional(data.get("adresse"))
        if is_val_err(ad):
            flash(ad["_error"], "error")
            return (
                render_template(
                    "inscription_agence.html",
                    active_nav="auth",
                    old=old,
                ),
                400,
            )
        vi = validate_ville_optional(data.get("ville"))
        if is_val_err(vi):
            flash(vi["_error"], "error")
            return (
                render_template(
                    "inscription_agence.html",
                    active_nav="auth",
                    old=old,
                ),
                400,
            )
        de = validate_description_optional(data.get("description"))
        if is_val_err(de):
            flash(de["_error"], "error")
            return (
                render_template(
                    "inscription_agence.html",
                    active_nav="auth",
                    old=old,
                ),
                400,
            )

        if Agence.query.filter_by(email=data["email"]).first():
            flash("Cette adresse e-mail est déjà utilisée.", "error")
            return (
                render_template(
                    "inscription_agence.html",
                    active_nav="auth",
                    old=old,
                ),
                409,
            )

        ag = Agence(
            nom=extra_nom,
            email=data["email"],
            telephone=data.get("telephone"),
            adresse=ad,
            ville=vi,
            description=de,
            statut="en_attente",
        )
        ag.set_password(data["password"])
        try:
            db.session.add(ag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Cette adresse e-mail est déjà utilisée.", "error")
            return (
                render_template(
                    "inscription_agence.html",
                    active_nav="auth",
                    old=old,
                ),
                409,
            )
        login_session(KIND_AGENCE, ag.id)
        flash("Demande d’inscription agence enregistrée (en attente de validation).", "success")
        return redirect(url_for("web.espace_agence"))

    return render_template(
        f"inscription_{role}.html",
        active_nav="auth",
        old={},
    )


@web_bp.post("/deconnexion")
def deconnexion():
    logout_session()
    return redirect(url_for("web.home"))


# --------------------------------------------------------------------------- #
# Annuaire (session web requise)
# --------------------------------------------------------------------------- #
@web_bp.route("/agences")
@login_required_web
def agences_list():
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (TypeError, ValueError):
        page = 1
    try:
        per_page = min(max(1, int(request.args.get("per_page", 12))), 100)
    except (TypeError, ValueError):
        per_page = 12

    ville = (request.args.get("ville") or "").strip() or None

    query = Agence.query.filter_by(statut="active")
    if ville:
        query = query.filter(Agence.ville.ilike(f"%{ville}%"))

    pagination = query.order_by(Agence.nom.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "agencies.html",
        active_nav="agencies",
        items=pagination.items,
        total=pagination.total,
        page=pagination.page,
        pages=pagination.pages,
        ville_filter=ville or "",
    )


@web_bp.route("/agences/<int:agence_id>")
@login_required_web
def agence_detail(agence_id):
    agence = db.session.get(Agence, agence_id)
    if not agence or agence.statut != "active":
        return render_template(
            "agency_not_found.html",
            active_nav="agencies",
        ), 404

    return render_template(
        "agency_detail.html",
        active_nav="agencies",
        agence=agence,
    )


# --------------------------------------------------------------------------- #
# Espace client
# --------------------------------------------------------------------------- #
@web_bp.route("/espace/client", methods=["GET"])
@require_session_kind(KIND_CLIENT)
def espace_client():
    cl = get_session_client()
    if not cl:
        logout_session()
        return redirect(url_for("web.home"))
    n_res = Reservation.query.filter_by(id_client=cl.id).count()
    return render_template(
        "dashboard_client.html",
        active_nav="espace_client",
        client=cl,
        n_reservations=n_res,
    )


@web_bp.route("/espace/client/profil", methods=["POST"])
@require_session_kind(KIND_CLIENT)
def espace_client_profil():
    cl = get_session_client()
    if not cl:
        return redirect(url_for("web.home"))

    nom = validate_name_person(request.form.get("nom", ""), "Nom")
    prenom = validate_name_person(request.form.get("prenom", ""), "Prénom")
    tel = validate_phone_optional(request.form.get("telephone"))

    for v in (nom, prenom, tel):
        if is_val_err(v):
            flash(v["_error"], "error")
            return redirect(url_for("web.espace_client"))

    cl.nom = nom
    cl.prenom = prenom
    cl.telephone = tel
    db.session.commit()
    flash("Profil mis à jour.", "success")
    return redirect(url_for("web.espace_client"))


@web_bp.route("/espace/client/mot-de-passe", methods=["POST"])
@require_session_kind(KIND_CLIENT)
def espace_client_password():
    cl = get_session_client()
    if not cl:
        return redirect(url_for("web.home"))

    schema = ChangePasswordSchema()
    schema.context = {"ancien_password": request.form.get("ancien_password")}
    try:
        data = schema.load(
            {
                "ancien_password": request.form.get("ancien_password", ""),
                "nouveau_password": request.form.get("nouveau_password", ""),
            }
        )
    except ValidationError as e:
        flash(" · ".join(str(x[0]) for x in e.messages.values()), "error")
        return redirect(url_for("web.espace_client"))

    if not cl.check_password(data["ancien_password"]):
        flash("Ancien mot de passe incorrect.", "error")
        return redirect(url_for("web.espace_client"))

    cl.set_password(data["nouveau_password"])
    db.session.commit()
    flash("Mot de passe mis à jour.", "success")
    return redirect(url_for("web.espace_client"))


# --------------------------------------------------------------------------- #
# Espace agence
# --------------------------------------------------------------------------- #
@web_bp.route("/espace/agence", methods=["GET"])
@require_session_kind(KIND_AGENCE)
def espace_agence():
    ag = get_session_agence()
    if not ag:
        logout_session()
        return redirect(url_for("web.home"))
    n_bus = Bus.query.filter_by(id_agence=ag.id).count()
    n_traj = Trajet.query.filter_by(id_agence=ag.id).count()
    return render_template(
        "dashboard_agence.html",
        active_nav="espace_agence",
        agence=ag,
        n_bus=n_bus,
        n_trajets=n_traj,
    )


@web_bp.route("/espace/agence/profil", methods=["POST"])
@require_session_kind(KIND_AGENCE)
def espace_agence_profil():
    ag = get_session_agence()
    if not ag:
        return redirect(url_for("web.home"))

    try:
        data = UpdateProfileSchema().load(
            {
                "nom": request.form.get("nom"),
                "telephone": request.form.get("telephone") or None,
                "adresse": request.form.get("adresse") or None,
                "ville": request.form.get("ville") or None,
                "description": request.form.get("description") or None,
            },
            partial=True,
        )
    except ValidationError as e:
        flash(" · ".join(f"{k}: {v}" for k, v in e.messages.items()), "error")
        return redirect(url_for("web.espace_agence"))

    for field, value in data.items():
        setattr(ag, field, value)
    db.session.commit()
    flash("Profil enregistré.", "success")
    return redirect(url_for("web.espace_agence"))


@web_bp.route("/espace/agence/mot-de-passe", methods=["POST"])
@require_session_kind(KIND_AGENCE)
def espace_agence_password():
    ag = get_session_agence()
    if not ag:
        return redirect(url_for("web.home"))

    schema = ChangePasswordSchema()
    schema.context = {"ancien_password": request.form.get("ancien_password")}
    try:
        data = schema.load(
            {
                "ancien_password": request.form.get("ancien_password", ""),
                "nouveau_password": request.form.get("nouveau_password", ""),
            }
        )
    except ValidationError as e:
        flash(" · ".join(str(x[0]) for x in e.messages.values()), "error")
        return redirect(url_for("web.espace_agence"))

    if not ag.check_password(data["ancien_password"]):
        flash("Ancien mot de passe incorrect.", "error")
        return redirect(url_for("web.espace_agence"))

    ag.set_password(data["nouveau_password"])
    db.session.commit()
    flash("Mot de passe mis à jour.", "success")
    return redirect(url_for("web.espace_agence"))


@web_bp.route("/espace/agence/logo", methods=["POST"])
@require_session_kind(KIND_AGENCE)
def espace_agence_logo():
    ag = get_session_agence()
    if not ag:
        return redirect(url_for("web.home"))

    if "logo" not in request.files:
        flash("Aucun fichier.", "error")
        return redirect(url_for("web.espace_agence"))

    file = request.files["logo"]
    if not file.filename:
        flash("Fichier vide.", "error")
        return redirect(url_for("web.espace_agence"))

    if not allowed_file(file.filename):
        flash("Format non autorisé (png, jpg, jpeg, webp).", "error")
        return redirect(url_for("web.espace_agence"))

    try:
        filename = save_logo(file)
    except Exception:  # noqa: BLE001
        current_app.logger.exception("Logo upload failed")
        flash("Impossible d’enregistrer le logo.", "error")
        return redirect(url_for("web.espace_agence"))

    ag.logo = filename
    db.session.commit()
    flash("Logo mis à jour.", "success")
    return redirect(url_for("web.espace_agence"))


# --------------------------------------------------------------------------- #
# Espace administrateur
# --------------------------------------------------------------------------- #
@web_bp.route("/espace/admin", methods=["GET"])
@require_session_kind(KIND_ADMIN)
def espace_admin():
    ad = get_session_admin()
    if not ad:
        logout_session()
        return redirect(url_for("web.home"))

    agences = Agence.query.order_by(Agence.date_creation.desc()).all()
    n_clients = Client.query.count()
    n_agences = Agence.query.count()

    return render_template(
        "dashboard_admin.html",
        active_nav="espace_admin",
        admin=ad,
        agences=agences,
        n_clients=n_clients,
        n_agences=n_agences,
    )


@web_bp.route("/espace/admin/agence/<int:aid>/statut", methods=["POST"])
@require_session_kind(KIND_ADMIN)
def espace_admin_statut(aid):
    if not get_session_admin():
        return redirect(url_for("web.home"))

    statut = (request.form.get("statut") or "").strip()
    if statut not in ("active", "suspendue", "en_attente"):
        flash("Statut invalide.", "error")
        return redirect(url_for("web.espace_admin"))

    ag = db.session.get(Agence, aid)
    if not ag:
        flash("Agence introuvable.", "error")
        return redirect(url_for("web.espace_admin"))

    ag.statut = statut
    db.session.commit()
    flash("Statut mis à jour.", "success")
    return redirect(url_for("web.espace_admin"))


# Compat : anciennes URL (redirections)
@web_bp.route("/compte")
def compte_redirect():
    if session_kind() == KIND_AGENCE:
        return redirect(url_for("web.espace_agence"))
    if session_kind() == KIND_CLIENT:
        return redirect(url_for("web.espace_client"))
    if session_kind() == KIND_ADMIN:
        return redirect(url_for("web.espace_admin"))
    return redirect(url_for("web.home"))


@web_bp.route("/connexion")
def connexion_legacy():
    return redirect(url_for("web.home"))


@web_bp.route("/inscription")
def inscription_legacy():
    return redirect(url_for("web.home"))
