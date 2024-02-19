from flask import redirect, render_template, request, session, g, url_for
from database import db
from utils.authentication import authenticate
import uuid
from utils.validator import Validator


@authenticate
def create_appointment():
    if g.get("user_data") is None:
        return redirect("/login")
    data = request.form
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, image, name, location, timing, price_per_person, small_description, description, rating, slug FROM vaccines WHERE id=%s", [data["vaccine_id"]])

    vaccine = cursor.fetchone()

    validator = (Validator(data)
                 .field("patent_name")
                 .required("Please enter patent's name")
                 .max_length(50, "patent's name must be less than 50 characters")
                 .field("patent_age")
                 .required("Please enter patent's age")
                 .validate(lambda age: int(age) <= 100 and int(age) >= 3, "Patent age must be older then 3 years old")
                 .field("gender")
                 .required("Please select patent's gender"))

    vaccine_details = {
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
    }

    if validator.errors.__len__() > 0:
        return render_template("vaccine-details.html", user=g.get("user_data"), vaccine=vaccine_details, errors=validator.errors, **validator.data)

    transaction_id = str(uuid.uuid4()).replace('-', '')

    cursor.execute(
        "INSERT INTO appointments(user_id, vaccine_id ,name, age, gender, transaction_id, appointment_status, total_price) VALUES (%s, %s, %s, %s, %s, %s ,'confirmed', %s)", (data["user_id"], data["vaccine_id"], validator.data['patent_name'], validator.data['patent_age'], validator.data['gender'], transaction_id, vaccine_details['price_per_person']))

    cursor.close()
    db.commit()
    return render_template("/confirmation.html", details={
        **vaccine_details,
        "transaction_id": transaction_id
    }, user=g.get("user_data"))


@authenticate
def render_appointments():
    if g.get("user_data") is None:
        return redirect("/login")

    user = g.get("user_data")
    cursor = db.cursor()

    cursor.execute(
        "SELECT vaccines.image, vaccines.name, vaccines.location, vaccines.timing, appointments.created_at, appointments.total_price, appointments.transaction_id, appointments.appointment_status, appointments.id FROM vaccines JOIN appointments ON vaccines.id = appointments.vaccine_id WHERE appointments.user_id=%s", [user["id"]])

    appointments = cursor.fetchall()
    cursor.close()
    appointment_list = []

    for appointment in appointments:
        formatted_date = appointment[4].strftime("%I:%M %p %d %b %Y")

        appointment_list.append({
            "image": appointment[0],
            "name": appointment[1],
            "location": appointment[2],
            "timing": appointment[3],
            "created_at": formatted_date,
            "total_price": appointment[5],
            "transaction_id": appointment[6],
            "appointment_status": appointment[7],
            "id": appointment[8]
        })

    return render_template("appointments.html", user=user, appointments=appointment_list)


@authenticate
def cancel_appointment(appointment_id):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE appointments SET appointment_status = 'cancelled' WHERE id =%s", [appointment_id])
    cursor.close()
    return redirect("/appointments")
