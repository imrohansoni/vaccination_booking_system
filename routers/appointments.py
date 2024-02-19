from controllers.appointment_controller import create_appointment, render_appointments, cancel_appointment
from flask import Blueprint

appointment_bp = Blueprint("bookings", __name__)


@appointment_bp.post("/")
def create_appointment_route():
    return create_appointment()


@appointment_bp.get("/")
def render_appointments_route():
    return render_appointments()


@appointment_bp.get("/<int:appointment_id>/cancel")
def cancel_appointment_route(appointment_id):
    return cancel_appointment(appointment_id)
