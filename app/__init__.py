import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        # Make sure uploads dir exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Import models so SQLAlchemy knows about them before creating tables
        from app import models
        db.create_all()
        
        # Seed a default admin user if the database is empty (crucial for Vercel)
        from app.models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@vetcare.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            

    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.appointments import appointments_bp
    from app.routes.pets import pets_bp
    from app.routes.billing import billing_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(pets_bp, url_prefix='/pets')
    app.register_blueprint(billing_bp, url_prefix='/billing')

    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('auth.login'))

    return app
