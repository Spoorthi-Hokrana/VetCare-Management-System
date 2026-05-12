from flask import Blueprint, render_template, make_response, send_file
from flask_login import login_required
from app.models import Invoice, InvoiceItem
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from datetime import datetime

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/')
@login_required
def index():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return render_template('billing/index.html', invoices=invoices)

@billing_bp.route('/invoice/<int:invoice_id>/pdf')
@login_required
def download_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Create PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "VetCare Clinic")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, "123 Animal Lane, Pet City")
    c.drawString(50, height - 85, "Phone: (555) 123-4567")
    
    # Invoice Details
    c.setFont("Helvetica-Bold", 16)
    c.drawString(400, height - 50, "INVOICE")
    
    c.setFont("Helvetica", 12)
    c.drawString(400, height - 70, f"Invoice #: {invoice.id:04d}")
    c.drawString(400, height - 85, f"Date: {invoice.created_at.strftime('%Y-%m-%d')}")
    c.drawString(400, height - 100, f"Status: {invoice.status}")
    
    # Client Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 130, "Bill To:")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 145, f"Owner: {invoice.appointment.pet.owner.name}")
    c.drawString(50, height - 160, f"Pet: {invoice.appointment.pet.name}")
    
    # Table Header
    y = height - 200
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Description")
    c.drawString(450, y, "Amount")
    c.line(50, y - 5, 550, y - 5)
    
    # Items
    y -= 25
    c.setFont("Helvetica", 12)
    for item in invoice.items:
        c.drawString(50, y, item.description)
        c.drawString(450, y, f"${item.amount:.2f}")
        y -= 20
        
    c.line(50, y, 550, y)
    y -= 20
    
    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(350, y, "Total Amount:")
    c.drawString(450, y, f"${invoice.total_amount:.2f}")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Thank you for trusting VetCare with your pet's health!")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'invoice_{invoice.id}.pdf', mimetype='application/pdf')

