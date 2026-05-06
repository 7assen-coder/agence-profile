from marshmallow import Schema, fields, validate, validates, ValidationError

from app.utils.input_regex import validate_email, validate_phone_optional, is_val_err


class RegisterSchema(Schema):
    nom = fields.String(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=128))
    telephone = fields.String(required=False, validate=validate.Length(max=8))
    adresse = fields.String(required=False, validate=validate.Length(max=200))
    ville = fields.String(required=False, validate=validate.Length(max=80))
    description = fields.String(required=False)

    @validates("email")
    def strict_email(self, value):  # noqa: PLW0206 — fonction marshmallow
        r = validate_email(value or "")
        if is_val_err(r):
            raise ValidationError(r["_error"])

    @validates("telephone")
    def strict_phone_optional(self, value):  # noqa: PLW0206
        if value is None or str(value).strip() == "":
            return
        r = validate_phone_optional(str(value))
        if is_val_err(r):
            raise ValidationError(r["_error"])


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1))

    @validates("email")
    def strict_email_login(self, value):  # noqa: PLW0206
        r = validate_email(value or "")
        if is_val_err(r):
            raise ValidationError(r["_error"])


class UpdateProfileSchema(Schema):
    nom = fields.String(validate=validate.Length(min=2, max=100))
    telephone = fields.String(validate=validate.Length(max=8))
    adresse = fields.String(validate=validate.Length(max=200))
    ville = fields.String(validate=validate.Length(max=80))
    description = fields.String()

    @validates("telephone")
    def tel_optional_profile(self, value):  # noqa: PLW0206
        if value is None or str(value).strip() == "":
            return
        r = validate_phone_optional(str(value))
        if is_val_err(r):
            raise ValidationError(r["_error"])


class ChangePasswordSchema(Schema):
    ancien_password = fields.String(required=True)
    nouveau_password = fields.String(
        required=True, validate=validate.Length(min=8, max=128)
    )

    @validates("nouveau_password")
    def not_same(self, value, **kwargs):
        if value == self.context.get("ancien_password"):
            raise ValidationError("Le nouveau mot de passe doit être différent.")


class AdminUpdateStatutSchema(Schema):
    statut = fields.String(
        required=True, validate=validate.OneOf(["active", "suspendue", "en_attente"])
    )
