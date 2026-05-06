from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from ..extensions import db
from ..models import Agence


def _split_identity(raw):
    if raw is None:
        return None, None
    s = str(raw)
    if ":" not in s:
        return None, None
    kind, _, rest = s.partition(":")
    return kind, rest


def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify(error="forbidden"), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def current_agence():
    kind, rest = _split_identity(get_jwt_identity())
    if kind != "agence":
        return None
    try:
        aid = int(rest)
    except (TypeError, ValueError):
        return None
    return db.session.get(Agence, aid)
