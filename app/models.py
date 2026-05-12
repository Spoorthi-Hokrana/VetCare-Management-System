from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='receptionist') # admin, doctor, receptionist
    
    # Relationships
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialty = db.Column(db.String(100))
    working_hours = db.Column(db.String(100), default='9:00 AM - 5:00 PM')
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class PetOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    pets = db.relationship('Pet', backref='owner', lazy=True, cascade="all, delete-orphan")

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('pet_owner.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    photo = db.Column(db.String(255), default='default_pet.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='pet', lazy=True, cascade="all, delete-orphan")
    vaccinations = db.relationship('Vaccination', backref='pet', lazy=True, cascade="all, delete-orphan")

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='Scheduled') # Scheduled, In Progress, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    medical_record = db.relationship('MedicalRecord', backref='appointment', uselist=False, cascade="all, delete-orphan")
    invoice = db.relationship('Invoice', backref='appointment', uselist=False, cascade="all, delete-orphan")

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    prescriptions = db.relationship('Prescription', backref='medical_record', lazy=True, cascade="all, delete-orphan")

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_record.id'), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text)

class Vaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    vaccine_name = db.Column(db.String(100), nullable=False)
    date_given = db.Column(db.Date, nullable=False)
    next_due_date = db.Column(db.Date)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    status = db.Column(db.String(20), default='Unpaid') # Unpaid, Partial, Paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade="all, delete-orphan")
    
    @property
    def total_amount(self):
        return sum(item.amount for item in self.items)

class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
