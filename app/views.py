from flask import Blueprint, render_template, abort
from .models import get_all_bus, get_bus, get_places_par_bus, get_stats

views_bp = Blueprint("views", __name__)


@views_bp.get("/")
def index():
    stats = get_stats()
    bus_list = get_all_bus()
    return render_template("index.html", stats=stats, bus_list=bus_list)


@views_bp.get("/bus/<int:bus_id>")
def detail_bus(bus_id):
    bus = get_bus(bus_id)
    if not bus:
        abort(404)
    places = get_places_par_bus(bus_id)
    return render_template("detail_bus.html", bus=bus, places=places)


@views_bp.app_errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404