from marshmallow import Schema, fields, validate, validates, ValidationError


class RegisterSchema(Schema):
    nom = fields.String(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=128))
    telephone = fields.String(required=False, validate=validate.Length(max=30))
    adresse = fields.String(required=False, validate=validate.Length(max=255))
    ville = fields.String(required=False, validate=validate.Length(max=80))
    description = fields.String(required=False)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1))


class UpdateProfileSchema(Schema):
    nom = fields.String(validate=validate.Length(min=2, max=120))
    telephone = fields.String(validate=validate.Length(max=30))
    adresse = fields.String(validate=validate.Length(max=255))
    ville = fields.String(validate=validate.Length(max=80))
    description = fields.String()


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
