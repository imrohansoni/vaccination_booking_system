from flask import Blueprint
from controllers.vaccine_controller import render_vaccines, render_vaccine_details


vaccine_bp = Blueprint("vaccines", __name__)


@vaccine_bp.get("/")
def get_vaccines_route():
    return render_vaccines()


@vaccine_bp.get("/<string:vaccine_slug>")
def get_tour_details(vaccine_slug):
    return render_vaccine_details(vaccine_slug)
