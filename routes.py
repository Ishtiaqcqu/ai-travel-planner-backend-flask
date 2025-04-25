from flask import Blueprint, jsonify, current_app, request
import google.generativeai as genai
import psycopg2
from models import db, User

api = Blueprint('api', __name__)

@api.route('/test-db', methods=['GET'])
def test_db_connection():
    """Test connection to PostgreSQL database."""
    try:
        # Test using SQLAlchemy connection
        db.session.execute('SELECT 1')
        
        # Test using direct psycopg2 connection to verify credentials
        conn = psycopg2.connect(
            host=current_app.config.get('SQLALCHEMY_DATABASE_URI').split('@')[1].split('/')[0].split(':')[0],
            database=current_app.config.get('SQLALCHEMY_DATABASE_URI').split('/')[-1],
            user=current_app.config.get('SQLALCHEMY_DATABASE_URI').split('://')[1].split(':')[0],
            password=current_app.config.get('SQLALCHEMY_DATABASE_URI').split(':')[2].split('@')[0]
        )
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully connected to PostgreSQL database'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to connect to database: {str(e)}'
        }), 500

@api.route('/test-gemini', methods=['GET'])
def test_gemini_connection():
    """Test connection to Gemini API."""
    try:
        # Configure the API key
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                'status': 'error',
                'message': 'Gemini API key not configured'
            }), 400
        
        # Initialize Gemini API
        genai.configure(api_key=api_key)
        
        # Test the API key with a simple call
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Hello, this is a test.")
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully connected to Gemini API',
            'test_response': response.text
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to connect to Gemini API: {str(e)}'
        }), 500

@api.route('/register', methods=['POST'])
def register_user():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Extract user details
        fullName = data.get('fullName')
        email = data.get('email')
        role = data.get('role', 'Member')
        
        # Validate required fields
        if not fullName or not email:
            return jsonify({
                'status': 'error',
                'message': 'Full name and email are required'
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'status': 'error',
                'message': 'User with this email already exists'
            }), 409
        
        # Create new user
        new_user = User(
            fullName=fullName,
            email=email,
            role=role
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Data saved successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to register user: {str(e)}'
        }), 500

@api.route('/verifylogin', methods=['POST'])
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