import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.config.config import Config
from app.models import init_app

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Log database connection string (hiding password)
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri:
        # Safely log DB connection info without exposing password
        censored_uri = db_uri.replace(os.environ.get('DB_PASSWORD', ''), '****')
        logger.info(f"Database URI: {censored_uri}")
    else:
        logger.error("Database URI is not configured!")
    
    # Initialize extensions
    CORS(app)
    logger.info("CORS initialized")
    
    try:
        init_app(app)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
    
    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.health_controller import health_bp
    from app.controllers.gemini_controller import gemini_bp
    from app.controllers.adminlte_controller import adminlte_bp
    from app.controllers.description_history_controller import history_bp
    from app.controllers.budget_history_controller import budget_history_bp
    from app.controllers.translation_history_controller import translation_history_bp
    from app.controllers.trip_history_controller import trip_history_bp
    from app.controllers.profile_controller import profile_bp
    from app.controllers.travel_plan_controller import travel_plan_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(gemini_bp, url_prefix='/api')
    app.register_blueprint(adminlte_bp, url_prefix='/admin')
    app.register_blueprint(history_bp, url_prefix='/api')
    app.register_blueprint(budget_history_bp, url_prefix='/api')
    app.register_blueprint(translation_history_bp, url_prefix='/api')
    app.register_blueprint(trip_history_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(travel_plan_bp, url_prefix='/api')
    
    logger.info("API routes registered")
    
    return app 