import os
from flask import Flask, jsonify
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

    from .models.agence import Agence  # noqa: F401

    from .routes.auth_routes import auth_bp
    from .routes.agence_routes import agence_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(agence_bp, url_prefix="/api/agences")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", module="gestion-profil-agence")

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="resource_not_found"), 404

    @app.errorhandler(413)
    def too_large(_):
        return jsonify(error="file_too_large"), 413

    @app.errorhandler(500)
    def server_error(_):
        return jsonify(error="internal_server_error"), 500

    return app
