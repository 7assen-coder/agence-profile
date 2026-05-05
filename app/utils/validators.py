import re

def is_required(value):
    return value is not None and str(value).strip() != ""

def is_valid_email(email):
    if not is_required(email):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    if not is_required(phone):
        return False
    pattern = r"^[0-9+\s-]{8,20}$"
    return re.match(pattern, phone) is not None

def is_positive_number(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False

def is_valid_place_number(numero):
    try:
        numero = int(numero)
        return 1 <= numero <= 12
    except (TypeError, ValueError):
        return False

def is_valid_horaire(horaire):
    return horaire in ["matin", "apres_midi"]

def is_valid_status_reservation(status):
    return status in ["en_attente", "confirmee", "annulee"]
