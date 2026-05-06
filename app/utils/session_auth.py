from functools import wraps

from flask import redirect, request, session, url_for

from ..extensions import db
from ..models import Administrateur, Client, Agence

SESSION_KIND = "auth_kind"
SESSION_ID = "auth_id"

KIND_CLIENT = "client"
KIND_AGENCE = "agence"
KIND_ADMIN = "admin"


def login_session(kind: str, pk: int) -> None:
    session[SESSION_KIND] = kind
    session[SESSION_ID] = pk
    session.permanent = True


def logout_session() -> None:
    session.pop(SESSION_KIND, None)
    session.pop(SESSION_ID, None)


def session_kind() -> str | None:
    return session.get(SESSION_KIND)


def session_user_id() -> int | None:
    uid = session.get(SESSION_ID)
    if uid is None:
        return None
    try:
        return int(uid)
    except (TypeError, ValueError):
        return None


def get_session_client():
    if session_kind() != KIND_CLIENT:
        return None
    uid = session_user_id()
    if uid is None:
        return None
    return db.session.get(Client, uid)


def get_session_agence():
    """Compatibilité templates : compte agence uniquement."""
    if session_kind() != KIND_AGENCE:
        return None
    uid = session_user_id()
    if uid is None:
        return None
    return db.session.get(Agence, uid)


def get_session_admin():
    if session_kind() != KIND_ADMIN:
        return None
    uid = session_user_id()
    if uid is None:
        return None
    return db.session.get(Administrateur, uid)


def require_session_kind(*kinds):
    def deco(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if session_kind() not in kinds:
                return redirect(url_for("web.home"))
            return fn(*args, **kwargs)

        return wrapped

    return deco


def safe_redirect_target(target: str | None, default_endpoint: str) -> str:
    if (
        target
        and isinstance(target, str)
        and target.startswith("/")
        and not target.startswith("//")
    ):
        return target
    return url_for(default_endpoint)


def json_or_session_required():
    """API : accès si session web (client/agence/admin) ou JWT valide."""
    from flask import jsonify
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    from flask_jwt_extended.exceptions import JWTExtendedException

    if session_kind():
        return None
    try:
        verify_jwt_in_request(optional=True)
    except JWTExtendedException:
        return jsonify(error="authentication_required"), 401
    if get_jwt_identity() is None:
        return jsonify(error="authentication_required"), 401
    return None


def login_required_web(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if session_kind() is None:
            return redirect(url_for("web.home", next=request.path))
        return fn(*args, **kwargs)

    return wrapped
