from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    """Initialize database with the app."""
    db.init_app(app)
    migrate.init_app(app, db)

# Import models to register them with SQLAlchemy
from app.models.user import User
from app.models.example import Example
from app.models.description_history import DescriptionHistory
from app.models.budget_history import BudgetHistory
from app.models.translation_history import TranslationHistory
from app.models.trip_history import TripHistory
from app.models.admin import Admin
from app.models.api_hit import ApiHit
from app.models.app_config import AppConfig 