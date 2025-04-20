import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gemini API configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 