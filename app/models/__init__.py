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