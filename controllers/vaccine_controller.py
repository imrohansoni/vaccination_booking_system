from flask import render_template, g
from database import db
from utils.authentication import authenticate


@authenticate
def render_vaccines():
    cursor = db.cursor()
    cursor.execute(
        "SELECT image, name, location, timing, price_per_person, small_description, rating, slug FROM vaccines")
    vaccines = cursor.fetchall()
    vaccine_list = []
    for vaccine in vaccines:
        vaccine_list.append({
            "image": vaccine[0],
            "name": vaccine[1],
            "location": vaccine[2],
            "timing": vaccine[3],
            "price_per_person": vaccine[4],
            "small_description": vaccine[5],
            "rating": vaccine[6],
            "slug": vaccine[7]
        })
    cursor.close()
    return render_template("vaccines.html", user=g.get("user_data"), vaccines=vaccine_list, active_link="vaccines")


@authenticate
def render_vaccine_details(vaccine_slug):
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, image, name, location, timing, price_per_person, small_description, description, rating, slug FROM vaccines WHERE slug=%s", [vaccine_slug])
    vaccine = cursor.fetchone()
    vaccine_details = ({
        "id": vaccine[0],
        "image": vaccine[1],
        "name": vaccine[2],
        "location": vaccine[3],
        "timing": vaccine[4],
        "price_per_person": vaccine[5],
        "small_description": vaccine[6],
        "description": vaccine[7],
        "rating": vaccine[8],
        "slug": vaccine[9]
    })
    return render_template("vaccine-details.html", user=g.get("user_data"), vaccine=vaccine_details, active_link="vaccines")
