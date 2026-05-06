"""Validation côté serveur (regex Python) — pas de JavaScript."""
from __future__ import annotations

import re

# Alignés avec les attributs HTML pattern des formulaires
# Email : partie locale + fournisseur connu + extension (.com, .fr, .ma, co.uk, …)
_EMAIL_LOCAL = r"[a-zA-Z0-9._%+\-]+"
_EMAIL_HOST = (
    r"(?:gmail|googlemail|yahoo|ymail|rocketmail|hotmail|outlook|live|msn|"
    r"icloud|me|mac|protonmail|proton|gmx|mail|orange|free|sfr|laposte|wanadoo|"
    r"bbox|neuf|hey|zoho|aol|skynet|transport|agence)"
)
_EMAIL_TLD = (
    r"(?:com|net|org|fr|ma|mr|io|co|edu|gov|info|de|es|it|be|ch|ca|us|au|uk|"
    r"nl|pt|pl|cn|jp|br|mx|tn|dz|eu|ru|in|tv|biz|name|"
    r"co\.uk|com\.ma|net\.ma|ac\.ma)"
)

RX_EMAIL = re.compile(
    rf"^{_EMAIL_LOCAL}@{_EMAIL_HOST}\.{_EMAIL_TLD}$",
    re.IGNORECASE,
)

EMAIL_PATTERN_HTML = (
    rf"^{_EMAIL_LOCAL}@{_EMAIL_HOST}\.{_EMAIL_TLD}$"
)

RX_PASSWORD = re.compile(r"^.{8,128}$")
RX_NAME = re.compile(r"^[A-Za-zÀ-ÿ\u00C0-\u024F\s'\-]{2,100}$")
# Mobile MA/MR : 8 chiffres exactement, premier chiffre 2, 3 ou 4 (pas d’espaces ni + )
RX_PHONE = re.compile(r"^[234]\d{7}$")
PHONE_MOBILE_PATTERN_HTML = r"^[234][0-9]{7}$"
# CIN client : exactement 10 chiffres
RX_CIN = re.compile(r"^\d{10}$")
CIN_PATTERN_HTML = r"^[0-9]{10}$"
RX_AGENCE_NOM = re.compile(r"^[A-Za-zÀ-ÿ0-9\s'\-&.]{2,100}$")
RX_ADRESSE = re.compile(r"^[A-Za-zÀ-ÿ0-9\s'\-,.°/]{5,200}$")


def err(msg: str):
    return {"_error": msg}


def validate_email(v: str) -> str | dict:
    v = (v or "").strip()
    if not RX_EMAIL.match(v):
        return err(
            "Email invalide : utilisez une messagerie reconnue (ex. gmail, yahoo, "
            "outlook…) avec une extension valide (.com, .fr, .ma, .mr…)."
        )
    return v


def validate_password(v: str) -> str | dict:
    if not RX_PASSWORD.match(v or ""):
        return err("Mot de passe : 8 à 128 caractères.")
    return v


def validate_name_person(v: str, label: str = "Nom") -> str | dict:
    v = (v or "").strip()
    if not RX_NAME.match(v):
        return err(f"{label} : 2 à 100 lettres, espaces, tirets ou apostrophes.")
    return v


def validate_agence_nom(v: str) -> str | dict:
    v = (v or "").strip()
    if not RX_AGENCE_NOM.match(v):
        return err("Nom d’agence invalide (2 à 100 caractères).")
    return v


def validate_phone_optional(v: str | None) -> str | None | dict:
    if v is None or (v := v.strip()) == "":
        return None
    if not RX_PHONE.match(v):
        return err(
            "Téléphone : exactement 8 chiffres, le premier doit être 2, 3 ou 4."
        )
    return v


def validate_phone_required(v: str) -> str | dict:
    v = (v or "").strip()
    if not v:
        return err("Téléphone requis.")
    if not RX_PHONE.match(v):
        return err(
            "Téléphone : exactement 8 chiffres, le premier doit être 2, 3 ou 4."
        )
    return v


def validate_cin(v: str) -> str | dict:
    v = (v or "").strip()
    if not RX_CIN.match(v):
        return err("CIN : exactement 10 chiffres.")
    return v


def validate_adresse_optional(v: str | None) -> str | None | dict:
    if v is None or (v := v.strip()) == "":
        return None
    if not RX_ADRESSE.match(v):
        return err("Adresse invalide (5 à 200 caractères).")
    return v


def validate_ville_optional(v: str | None) -> str | None | dict:
    if v is None or (v := v.strip()) == "":
        return None
    if len(v) > 80:
        return err("Ville trop longue.")
    return v


def validate_description_optional(v: str | None) -> str | None | dict:
    if v is None:
        return None
    v = v.strip()
    if len(v) > 5000:
        return err("Description trop longue.")
    return v if v else None


def is_val_err(x) -> bool:
    return isinstance(x, dict) and "_error" in x
