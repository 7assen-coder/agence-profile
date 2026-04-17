from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from ..models.agence import Agence


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
    claims = get_jwt()
    agence_id = claims.get("sub") or claims.get("agence_id")
    if not agence_id:
        return None
    return Agence.query.get(int(agence_id))
