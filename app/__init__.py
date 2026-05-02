from flask import Flask
from .database import init_db
from .routes import places_bp


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DB_HOST="localhost",
        DB_USER="MDK",
        DB_PASSWORD="1234",
        DB_NAME="transport_reservation_v4",
    )

    if config:
        app.config.update(config)

    init_db()

    app.register_blueprint(places_bp, url_prefix="/places")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
