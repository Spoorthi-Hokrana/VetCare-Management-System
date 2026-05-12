import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-vet-app-secret'
    
    if os.environ.get('VERCEL') == '1':
        # Vercel's filesystem is read-only except for /tmp
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/vetclinic.db'
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'instance', 'vetclinic.db')
        UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail Config (Dummy for now)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 8025))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB max upload
