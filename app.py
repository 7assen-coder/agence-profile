from flask import Flask
from routes.disponibilites import bp_dispo
from routes.reservations import bp_resa
from routes.paiements import bp_paiement
from scheduler import demarrer_scheduler

app = Flask(__name__)
app.config["SECRET_KEY"] = "transport2025_secret"

app.register_blueprint(bp_dispo,    url_prefix="/api/disponibilites")
app.register_blueprint(bp_resa,     url_prefix="/api/reservations")
app.register_blueprint(bp_paiement, url_prefix="/api/paiements")

demarrer_scheduler()

if __name__ == "__main__":
    app.run(debug=True, port=5000)