from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, IntegerField, TextAreaField, DateField, TimeField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class StaffForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('doctor', 'Doctor'), ('receptionist', 'Receptionist'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Add Staff')

class PetOwnerForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Register Owner')

class PetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired(), Length(min=2, max=100)])
    species = SelectField('Species', choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Rabbit', 'Rabbit'), ('Bird', 'Bird'), ('Other', 'Other')], validators=[DataRequired()])
    breed = StringField('Breed', validators=[Length(max=50)])
    age = IntegerField('Age (Years)', validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    photo = FileField('Pet Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Register Pet')

class AddPetForm(PetForm):
    owner_id = SelectField('Owner', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Pet to Owner')

class AppointmentForm(FlaskForm):
    pet_id = SelectField('Pet', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    reason = StringField('Reason for Visit', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Book Appointment')

class MedicalRecordForm(FlaskForm):
    symptoms = TextAreaField('Symptoms', validators=[DataRequired()])
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    treatment = TextAreaField('Treatment')
    submit = SubmitField('Save Record')

class PrescriptionForm(FlaskForm):
    medicine_name = StringField('Medicine Name', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Prescription')

class VaccinationForm(FlaskForm):
    vaccine_name = StringField('Vaccine Name', validators=[DataRequired()])
    date_given = DateField('Date Given', format='%Y-%m-%d', validators=[DataRequired()])
    next_due_date = DateField('Next Due Date', format='%Y-%m-%d')
    submit = SubmitField('Log Vaccination')

class InvoiceForm(FlaskForm):
    status = SelectField('Payment Status', choices=[('Unpaid', 'Unpaid'), ('Partial', 'Partial'), ('Paid', 'Paid')], validators=[DataRequired()])
    submit = SubmitField('Update Status')

class InvoiceItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount ($)', validators=[DataRequired()])
    submit = SubmitField('Add Item')
