from flask import Flask
from .database import init_db
from .routes import places_bp
from .views import views_bp


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DB_HOST="localhost",
        DB_USER="MDK",
        DB_PASSWORD="1234",
        DB_NAME="transport_reservation_v4",
        SECRET_KEY="dev-secret-key",
    )

    if config:
        app.config.update(config)

    init_db(app)

    # API JSON
    app.register_blueprint(places_bp, url_prefix="/api/places")

    # Pages HTML (render_template)
    app.register_blueprint(views_bp)

    return app
