from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Appointment
from datetime import date

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/')
@login_required
def index():
    today = date.today()
    todays_appointments = Appointment.query.filter_by(date=today).order_by(Appointment.time).all()
    upcoming_appointments = Appointment.query.filter(Appointment.date > today).order_by(Appointment.date, Appointment.time).limit(10).all()
    
    return render_template('appointments/index.html', todays=todays_appointments, upcoming=upcoming_appointments)

@appointments_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    from flask import request, flash, redirect, url_for
    from app.forms import AppointmentForm
    from app.models import Pet, Doctor, db
    
    form = AppointmentForm()
    # Populate choices
    form.pet_id.choices = [(p.id, f"{p.name} ({p.owner.name})") for p in Pet.query.all()]
    form.doctor_id.choices = [(d.id, f"Dr. {d.user.username} - {d.specialty}") for d in Doctor.query.all()]
    
    if request.method == 'GET':
        pet_id = request.args.get('pet_id')
        if pet_id:
            form.pet_id.data = int(pet_id)
    
    if request.method == 'POST' and form.validate():
        appt = Appointment(
            pet_id=form.pet_id.data,
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            time=form.time.data,
            reason=form.reason.data,
            status='Scheduled'
        )
        db.session.add(appt)
        db.session.commit()
        flash('Appointment successfully booked!', 'success')
        return redirect(url_for('appointments.index'))
        
    return render_template('appointments/book.html', form=form)
