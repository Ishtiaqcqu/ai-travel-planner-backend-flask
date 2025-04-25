from flask import Blueprint, jsonify
import logging
from sqlalchemy import text
from app.models import db

logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Service is running'})

@health_bp.route('/test-db', methods=['GET'])
def test_db_connection():
    """Test connection to PostgreSQL database."""
    try:
        logger.info("Testing database connection...")
        # Test using SQLAlchemy connection
        db.session.execute(text('SELECT 1'))
        logger.info("SQLAlchemy connection test successful")
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully connected to PostgreSQL database'
        })
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to connect to database: {str(e)}'
        }), 500 