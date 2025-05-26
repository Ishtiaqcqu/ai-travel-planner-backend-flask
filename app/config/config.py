import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded in config")

class Config:
    """Base configuration for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour in seconds
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Get database configuration from environment variables
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    
    # Check if all required database environment variables are set
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        missing_vars = [var for var, val in [
            ('DB_USER', DB_USER),
            ('DB_PASSWORD', DB_PASSWORD),
            ('DB_HOST', DB_HOST),
            ('DB_NAME', DB_NAME)
        ] if not val]
        logger.error(f"Missing required database environment variables: {', '.join(missing_vars)}")
        # If in production, this could be a critical error
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError(f"Missing required database environment variables: {', '.join(missing_vars)}")
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gemini API configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 
    if not GEMINI_API_KEY:
        logger.warning("Gemini API key not found in environment variables") 