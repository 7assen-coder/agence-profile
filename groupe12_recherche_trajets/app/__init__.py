from flask import Flask
from flask_cors import CORS
from app.routes.recherche_routes import bp as bp_recherche

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(bp_recherche)
    return app
