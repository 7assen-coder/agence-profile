import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template
from .config import Config
from .extensions import db, migrate, jwt, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from .models import (  # noqa: F401
        Administrateur,
        Agence,
        Bus,
        Client,
        Paiement,
        Place,
        Reservation,
        Trajet,
        Ville,
    )

    from .routes.auth_routes import auth_bp
    from .routes.agence_routes import agence_bp
    from .routes.web_routes import web_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(agence_bp, url_prefix="/api/agences")
    app.register_blueprint(web_bp)

    @app.context_processor
    def _inject_session():  # noqa: WPS430
        from .utils import session_auth as sa

        return {
            "session_kind": sa.session_kind(),
            "session_client": sa.get_session_client(),
            "session_agence": sa.get_session_agence(),
            "session_admin": sa.get_session_admin(),
            "agence_session": sa.get_session_agence(),
        }

    @app.context_processor
    def _template_globals():  # noqa: WPS430
        from .utils.input_regex import (
            CIN_PATTERN_HTML,
            EMAIL_PATTERN_HTML,
            PHONE_MOBILE_PATTERN_HTML,
        )

        return {
            "current_year": datetime.now(timezone.utc).year,
            "pattern_email": EMAIL_PATTERN_HTML,
            "pattern_phone_mobile": PHONE_MOBILE_PATTERN_HTML,
            "pattern_cin": CIN_PATTERN_HTML,
        }

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", module="gestion-profil-agence")

    @app.errorhandler(404)
    def not_found(_):
        if request.path.startswith("/api"):
            return jsonify(error="resource_not_found"), 404
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def too_large(_):
        return jsonify(error="file_too_large"), 413

    @app.errorhandler(500)
    def server_error(_):
        return jsonify(error="internal_server_error"), 500

    return app
