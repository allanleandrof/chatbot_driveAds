from flask import Flask
from config.settings import Config
import firebase_admin
from firebase_admin import credentials
import logging

def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Initialize Firebase
    cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    
    # Register blueprints
    from app.routes.whatsapp import whatsapp_bp
    app.register_blueprint(whatsapp_bp)
    
    return app