from flask import Blueprint, request, jsonify
import logging
from app.models import db
from app.models.user import User

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    """Register a new user."""
    try:
        logger.info("Processing user registration request")
        data = request.get_json()
        logger.debug(f"Registration data received: {data}")
        
        # Extract user details
        fullName = data.get('fullName')
        email = data.get('email')
        role = data.get('role', 'Member')
        
        logger.info(f"Registering user: {email}, role: {role}")
        
        # Validate required fields
        if not fullName or not email:
            logger.warning("Registration failed: Missing required fields")
            return jsonify({
                'status': 'error',
                'message': 'Full name and email are required'
            }), 400
        
        # Check if user already exists
        logger.info(f"Checking if user already exists: {email}")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            logger.warning(f"User already exists with email: {email}")
            return jsonify({
                'status': 'error',
                'message': 'User with this email already exists'
            }), 409
        
        # Create new user
        logger.info(f"Creating new user: {email}")
        new_user = User(
            fullName=fullName,
            email=email,
            role=role
        )
        
        # Save to database
        logger.info("Adding user to database session")
        db.session.add(new_user)
        
        logger.info("Committing user to database")
        db.session.commit()
        logger.info(f"User successfully registered: {email}")
        
        return jsonify({
            'status': 'success',
            'message': 'Data saved successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Registration failed with exception: {str(e)}")
        logger.exception("Detailed exception information:")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to register user: {str(e)}'
        }), 500

@auth_bp.route('/verifylogin', methods=['POST'])
def verify_login():
    """Verify user login based on email and role."""
    try:
        data = request.get_json()
        
        # Extract login details
        email = data.get('email')
        role = data.get('role')
        
        # Validate required fields
        if not email or not role:
            return jsonify({
                'status': 'error',
                'message': 'Email and role are required'
            }), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and role matches
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 401
            
        if user.role != role:
            return jsonify(False), 401
        
        return jsonify(True), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to verify login: {str(e)}'
        }), 500 