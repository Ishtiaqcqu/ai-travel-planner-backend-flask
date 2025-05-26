import logging
import subprocess
from sqlalchemy import text
from app.models import db

logger = logging.getLogger(__name__)

def run_flask_command(command):
    """Run a Flask command with subprocess."""
    try:
        logger.info(f"Running command: flask {command}")
        result = subprocess.run(f"flask {command}", shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Command succeeded: {result.stdout}")
            return True
        else:
            logger.error(f"Command failed with exit code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Exception running command: {str(e)}")
        return False

def init_migrations():
    """Initialize database migrations."""
    logger.info("Initializing database migrations...")
    return run_flask_command("db init")

def create_migration(message="Create tables"):
    """Create a database migration."""
    logger.info(f"Creating migration: {message}")
    return run_flask_command(f"db migrate -m \"{message}\"")

def upgrade_database():
    """Apply all database migrations."""
    logger.info("Upgrading database schema...")
    return run_flask_command("db upgrade")

def list_tables(app):
    """List all tables in the database."""
    logger.info("Listing tables in database...")
    with app.app_context():
        try:
            tables = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public'
            """)).fetchall()
            
            table_names = [table[0] for table in tables]
            logger.info(f"Tables in database: {table_names}")
            return table_names
        except Exception as e:
            logger.error(f"Error listing tables: {str(e)}")
            return [] 