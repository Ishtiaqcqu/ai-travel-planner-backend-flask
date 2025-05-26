from flask import Blueprint, request, jsonify
import logging
from app.models import db
from app.models.user import User
from app.utils.firebase_auth import verify_firebase_token
from app.utils.api_tracker import track_api_hit

logger = logging.getLogger(__name__)

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['PUT'])
@track_api_hit
def update_profile():
    """Update user profile information."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body must be JSON'}), 400

        # No authentication required for testing
        logger.info("Profile update request received (no authentication required)")

        # Validate required fields
        full_name = data.get('fullName')
        email = data.get('email')

        if not full_name:
            return jsonify({'success': False, 'error': 'fullName is required'}), 400
        if not email:
            return jsonify({'success': False, 'error': 'email is required'}), 400

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update user fields
        user.fullName = full_name
        
        # Update optional fields if provided
        if 'passportNumber' in data:
            user.passport_number = data.get('passportNumber')
        
        if 'travelPreferences' in data:
            user.travel_preferences = data.get('travelPreferences')

        # Save changes
        db.session.commit()
        logger.info(f"Profile updated successfully for user: {email}")

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        }), 200

    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Failed to update profile: {str(e)}'}), 500

@profile_bp.route('/profile', methods=['GET'])
@track_api_hit
def get_profile():
    """Fetch user profile information."""
    try:
        # Get email from query parameter
        email = request.args.get('email')
        
        if not email:
            return jsonify({'error': 'Email parameter is required'}), 400

        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        logger.info(f"Profile fetch request for user: {email}")

        # Return user profile data in the specified format
        profile_data = {
            'fullName': user.fullName,
            'email': user.email,
            'passportNumber': user.passport_number,
            'travelPreferences': user.travel_preferences
        }

        return jsonify({
            'success': True,
            'data': profile_data
        }), 200

    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}")
        return jsonify({'error': f'Failed to fetch profile: {str(e)}'}), 500 