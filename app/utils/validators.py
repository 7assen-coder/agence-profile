import re


def is_required(value):
    return value is not None and str(value).strip() != ""


def is_valid_email(email):
    if not is_required(email):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, str(email)) is not None


def is_valid_phone(phone):
    if not is_required(phone):
        return False
    pattern = r"^[0-9+\s-]{8,20}$"
    return re.match(pattern, str(phone)) is not None


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
    return horaire in ["matin", "apres_midi", "apres-midi"]


def is_valid_status_reservation(statut):
    return statut in ["en_attente", "reservee", "payee", "annulee"]


def is_valid_mode_paiement(mode):
    return mode in ["cash", "bankily", "sedad", "masrivi"]
def is_valid_id(value):
    try:
        return int(value) > 0
    except (TypeError, ValueError):
        return False


def is_valid_password(password):
    return is_required(password) and len(str(password)) >= 6


def is_valid_name(name):
    if not is_required(name):
        return False
    return len(str(name).strip()) >= 2


def is_valid_date(value):
    return is_required(value)


def is_valid_promotion_value(value):
    try:
        value = float(value)
        return 0 < value <= 100
    except (TypeError, ValueError):
        return False