from app.models import User, Doctor, PetOwner, Pet, Appointment, MedicalRecord, Prescription, Vaccination, Invoice, InvoiceItem
from datetime import datetime, date, time, timedelta
import random

def run_seed(db, bcrypt):
    # Only seed if the database is completely empty
    if User.query.first():
        return

    print("Seeding Users...")
    # Admin
    admin = User(username='admin', email='admin@vetcare.com', password=bcrypt.generate_password_hash('admin123').decode('utf-8'), role='admin')
    # Receptionist
    receptionist = User(username='reception', email='reception@vetcare.com', password=bcrypt.generate_password_hash('reception123').decode('utf-8'), role='receptionist')
    db.session.add_all([admin, receptionist])

    # Vets
    vet_data = [
        {'username': 'dr_smith', 'email': 'smith@vetcare.com', 'specialty': 'General Practice'},
        {'username': 'dr_jones', 'email': 'jones@vetcare.com', 'specialty': 'Surgery'},
        {'username': 'dr_williams', 'email': 'williams@vetcare.com', 'specialty': 'Dermatology'}
    ]
    
    doctors = []
    for v in vet_data:
        user = User(username=v['username'], email=v['email'], password=bcrypt.generate_password_hash('vet123').decode('utf-8'), role='doctor')
        db.session.add(user)
        db.session.flush() # To get user.id
        doctor = Doctor(user_id=user.id, specialty=v['specialty'])
        db.session.add(doctor)
        doctors.append(doctor)

    print("Seeding Pet Owners...")
    owners_data = [
        {'name': 'Alice Johnson', 'phone': '555-0101', 'email': 'alice@example.com', 'address': '123 Elm St'},
        {'name': 'Bob Smith', 'phone': '555-0102', 'email': 'bob@example.com', 'address': '456 Oak St'},
        {'name': 'Charlie Brown', 'phone': '555-0103', 'email': 'charlie@example.com', 'address': '789 Pine St'},
        {'name': 'Diana Prince', 'phone': '555-0104', 'email': 'diana@example.com', 'address': '101 Maple St'},
        {'name': 'Ethan Hunt', 'phone': '555-0105', 'email': 'ethan@example.com', 'address': '202 Birch St'}
    ]
    
    owners = []
    for o in owners_data:
        owner = PetOwner(**o)
        db.session.add(owner)
        owners.append(owner)
        
    db.session.flush()

    print("Seeding Pets...")
    pets_data = [
        {'owner_id': owners[0].id, 'name': 'Buddy', 'species': 'Dog', 'breed': 'Golden Retriever', 'age': 3, 'weight': 30.5},
        {'owner_id': owners[0].id, 'name': 'Mittens', 'species': 'Cat', 'breed': 'Siamese', 'age': 2, 'weight': 4.2},
        {'owner_id': owners[1].id, 'name': 'Rex', 'species': 'Dog', 'breed': 'German Shepherd', 'age': 5, 'weight': 35.0},
        {'owner_id': owners[2].id, 'name': 'Whiskers', 'species': 'Cat', 'breed': 'Persian', 'age': 4, 'weight': 5.1},
        {'owner_id': owners[2].id, 'name': 'Thumper', 'species': 'Rabbit', 'breed': 'Holland Lop', 'age': 1, 'weight': 1.8},
        {'owner_id': owners[3].id, 'name': 'Bella', 'species': 'Dog', 'breed': 'Poodle', 'age': 2, 'weight': 15.0},
        {'owner_id': owners[3].id, 'name': 'Luna', 'species': 'Cat', 'breed': 'Maine Coon', 'age': 3, 'weight': 6.5},
        {'owner_id': owners[4].id, 'name': 'Max', 'species': 'Dog', 'breed': 'Beagle', 'age': 4, 'weight': 12.0},
        {'owner_id': owners[4].id, 'name': 'Chloe', 'species': 'Cat', 'breed': 'Domestic Shorthair', 'age': 2, 'weight': 4.5},
        {'owner_id': owners[4].id, 'name': 'Oreo', 'species': 'Rabbit', 'breed': 'Netherland Dwarf', 'age': 1, 'weight': 1.2}
    ]
    
    pets = []
    for p in pets_data:
        pet = Pet(**p)
        db.session.add(pet)
        pets.append(pet)
        
    db.session.flush()

    print("Seeding Appointments, Records, and Invoices...")
    statuses = ['Scheduled', 'In Progress', 'Completed', 'Cancelled']
    reasons = ['Annual Checkup', 'Vaccination', 'Illness', 'Injury', 'Dental Cleaning']
    
    for i in range(15):
        pet = random.choice(pets)
        doctor = random.choice(doctors)
        days_offset = random.randint(-7, 7)
        appt_date = date.today() + timedelta(days=days_offset)
        appt_time = time(random.randint(9, 16), random.choice([0, 30]))
        status = 'Scheduled' if days_offset > 0 else random.choice(['Completed', 'Completed', 'Cancelled'])
        
        appointment = Appointment(pet_id=pet.id, doctor_id=doctor.id, date=appt_date, time=appt_time, reason=random.choice(reasons), status=status)
        db.session.add(appointment)
        db.session.flush()

        if status == 'Completed':
            record = MedicalRecord(
                appointment_id=appointment.id,
                symptoms='Routine visit' if 'Checkup' in appointment.reason else 'Patient reported discomfort.',
                diagnosis='Healthy' if 'Checkup' in appointment.reason else 'Minor infection.',
                treatment='Prescribed rest and medication.' if 'infection' in 'Minor infection' else 'None required.'
            )
            db.session.add(record)
            db.session.flush()
            
            if 'infection' in record.diagnosis:
                prescription = Prescription(
                    medical_record_id=record.id,
                    medicine_name='Amoxicillin',
                    dosage='250mg',
                    duration='7 days',
                    notes='Take with food'
                )
                db.session.add(prescription)

            if random.choice([True, False]):
                vaccination = Vaccination(
                    pet_id=pet.id,
                    vaccine_name=random.choice(['Rabies', 'Distemper', 'Parvovirus']),
                    date_given=appt_date,
                    next_due_date=appt_date + timedelta(days=365)
                )
                db.session.add(vaccination)

            invoice = Invoice(
                appointment_id=appointment.id,
                status=random.choice(['Paid', 'Unpaid', 'Partial'])
            )
            db.session.add(invoice)
            db.session.flush()
            
            db.session.add(InvoiceItem(invoice_id=invoice.id, description='Consultation Fee', amount=50.0))
            if 'Vaccination' in appointment.reason:
                db.session.add(InvoiceItem(invoice_id=invoice.id, description='Vaccine Adminstration', amount=35.0))
            if 'infection' in record.diagnosis:
                db.session.add(InvoiceItem(invoice_id=invoice.id, description='Medication', amount=25.0))

    db.session.commit()
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    from app import create_app, db, bcrypt
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate if running manually
        db.drop_all()
        db.create_all()
        run_seed(db, bcrypt)
