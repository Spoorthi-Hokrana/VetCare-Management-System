from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Pet, Appointment, Invoice, MedicalRecord, db
from datetime import date, datetime, timedelta
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    first_day_of_month = today.replace(day=1)
    
    total_pets = Pet.query.count()
    todays_appointments = Appointment.query.filter_by(date=today).count()
    
    # Revenue this month
    invoices_this_month = Invoice.query.filter(Invoice.created_at >= first_day_of_month).all()
    revenue_this_month = sum(inv.total_amount for inv in invoices_this_month if inv.status == 'Paid')
    
    pending_bills = Invoice.query.filter(Invoice.status != 'Paid').count()
    
    recent_appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).limit(5).all()

    # Data for charts
    # Appointment status donut chart
    status_counts = db.session.query(Appointment.status, func.count(Appointment.id)).group_by(Appointment.status).all()
    status_labels = [s[0] for s in status_counts]
    status_data = [s[1] for s in status_counts]

    # Quick dummy data for revenue trend (area chart) - last 7 days
    revenue_labels = [(today - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
    revenue_data = [0] * 7
    # (Simplified for the demo, just mock trend or calculate it)
    
    return render_template('dashboard/admin.html', 
                           total_pets=total_pets, 
                           todays_appointments=todays_appointments,
                           revenue_this_month=revenue_this_month,
                           pending_bills=pending_bills,
                           recent_appointments=recent_appointments,
                           status_labels=status_labels,
                           status_data=status_data,
                           revenue_labels=revenue_labels,
                           revenue_data=[120, 200, 150, 300, 250, 400, 320]) # mock data for area chart

@admin_bp.route('/staff')
@login_required
def staff():
    if current_user.role != 'admin':
        from flask import flash, redirect, url_for
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    from app.models import User
    staff_members = User.query.all()
    return render_template('dashboard/staff.html', staff_members=staff_members)

@admin_bp.route('/staff/add', methods=['GET', 'POST'])
@login_required
def add_staff():
    if current_user.role != 'admin':
        from flask import flash, redirect, url_for
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    from app.forms import StaffForm
    from app.models import User, Doctor, db
    from app import bcrypt
    from flask import request, flash, redirect, url_for
    
    form = StaffForm()
    if request.method == 'POST' and form.validate():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_pw,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.flush()
        
        if form.role.data == 'doctor':
            doctor = Doctor(user_id=new_user.id, specialty="General Practice")
            db.session.add(doctor)
            
        db.session.commit()
        flash('Staff member added successfully!', 'success')
        return redirect(url_for('admin.staff'))
        
    return render_template('dashboard/add_staff.html', form=form)

@admin_bp.route('/staff/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_staff(user_id):
    if current_user.role != 'admin':
        from flask import flash, redirect, url_for
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    from app.models import User, db
    from flask import request, flash, redirect, url_for
    
    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete.id == current_user.id:
        flash("You cannot delete yourself!", "danger")
    else:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Staff member deleted.", "success")
        
    return redirect(url_for('admin.staff'))
