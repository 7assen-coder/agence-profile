from flask import Flask, jsonify
from .config import Config
from .extensions import db, migrate, jwt, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from .models.reservation import Reservation  # noqa: F401

    from .routes.reservation_routes import reservation_bp
    app.register_blueprint(reservation_bp, url_prefix="/api/reservations")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", module="gestion-reservations")

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="resource_not_found"), 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify(error="internal_server_error"), 500

    return app
