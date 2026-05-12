from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import Pet, PetOwner, MedicalRecord, Vaccination, Appointment, db
from app.forms import PetForm, PetOwnerForm

pets_bp = Blueprint('pets', __name__)

@pets_bp.route('/')
@login_required
def index():
    # Simple list of pets
    pets = Pet.query.all()
    return render_template('pets/index.html', pets=pets)

@pets_bp.route('/profile/<int:pet_id>')
@login_required
def profile(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    # Get history
    history = Appointment.query.filter_by(pet_id=pet.id, status='Completed').order_by(Appointment.date.desc()).all()
    vaccinations = Vaccination.query.filter_by(pet_id=pet.id).order_by(Vaccination.date_given.desc()).all()
    
    return render_template('pets/profile.html', pet=pet, history=history, vaccinations=vaccinations)

@pets_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    owner_form = PetOwnerForm(prefix="owner")
    pet_form = PetForm(prefix="pet")
    
    if request.method == 'POST' and owner_form.validate() and pet_form.validate():
        # Check if owner exists by email or phone (simplified: just create new for demo)
        owner = PetOwner(
            name=owner_form.name.data,
            phone=owner_form.phone.data,
            email=owner_form.email.data,
            address=owner_form.address.data
        )
        db.session.add(owner)
        db.session.flush() # get ID
        
        pet = Pet(
            owner_id=owner.id,
            name=pet_form.name.data,
            species=pet_form.species.data,
            breed=pet_form.breed.data,
            age=pet_form.age.data,
            weight=pet_form.weight.data
        )
        db.session.add(pet)
        db.session.commit()
        
        flash(f'Successfully registered {pet.name}!', 'success')
        return redirect(url_for('pets.profile', pet_id=pet.id))
        
    return render_template('pets/register.html', owner_form=owner_form, pet_form=pet_form)

@pets_bp.route('/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    from app.forms import AddPetForm
    form = AddPetForm()
    form.owner_id.choices = [(o.id, f"{o.name} ({o.phone})") for o in PetOwner.query.all()]
    
    if request.method == 'POST' and form.validate():
        pet = Pet(
            owner_id=form.owner_id.data,
            name=form.name.data,
            species=form.species.data,
            breed=form.breed.data,
            age=form.age.data,
            weight=form.weight.data
        )
        db.session.add(pet)
        db.session.commit()
        
        flash(f'Successfully added {pet.name} to owner!', 'success')
        return redirect(url_for('pets.profile', pet_id=pet.id))
        
    return render_template('pets/add_pet.html', form=form)

@pets_bp.route('/edit/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)
    
    if request.method == 'POST' and form.validate():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.breed = form.breed.data
        pet.age = form.age.data
        pet.weight = form.weight.data
        db.session.commit()
        flash('Pet profile updated!', 'success')
        return redirect(url_for('pets.profile', pet_id=pet.id))
        
    return render_template('pets/edit.html', form=form, pet=pet)

@pets_bp.route('/vaccination/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def add_vaccination(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    from app.forms import VaccinationForm
    form = VaccinationForm()
    
    if request.method == 'POST' and form.validate():
        vac = Vaccination(
            pet_id=pet.id,
            vaccine_name=form.vaccine_name.data,
            date_given=form.date_given.data,
            next_due_date=form.next_due_date.data
        )
        db.session.add(vac)
        db.session.commit()
        flash('Vaccination record added!', 'success')
        return redirect(url_for('pets.profile', pet_id=pet.id))
        
    return render_template('pets/vaccination.html', form=form, pet=pet)

