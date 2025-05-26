#import all libries
from flask import Blueprint, jsonify, request
import logging
import uuid
from datetime import datetime
from app.models import db
from app.models.trip_history import TripHistory
from app.utils.api_tracker import track_api_hit

logger = logging.getLogger(__name__)

trip_history_bp = Blueprint('trip_history', __name__)

@trip_history_bp.route('/travel-history', methods=['GET'])
@track_api_hit
def get_travel_history():
    """Retrieve user's travel history via GET request with query parameter."""
    try:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Missing userId query parameter'
            }), 400

        # Query user's trip history, ordered by most recent first
        history_records = TripHistory.query.filter_by(user_id=user_id)\
                                          .order_by(TripHistory.timestamp.desc())\
                                          .all()

        # Convert to the expected format for frontend
        history_list = []
        for record in history_records:
            # Extract data from the stored format
            request_data = record.request_data or {}
            response_data = record.response_data or {}
            
            history_item = {
                'id': record.id,
                'destination': request_data.get('destination', ''),
                'preferences': request_data.get('preferences', ''),
                'budget': request_data.get('budget', ''),
                'language': request_data.get('language', 'english'),
                'travelPlan': response_data,
                'timestamp': record.timestamp.isoformat() if record.timestamp else record.created_at.isoformat()
            }
            history_list.append(history_item)

        return jsonify({
            'success': True,
            'data': {
                'history': history_list
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in /travel-history endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve travel history: {str(e)}'
        }), 500

@trip_history_bp.route('/trip-history', methods=['POST'])
@track_api_hit
def get_trip_history():
    """Retrieve user's trip planning history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON',
                'code': 'INVALID_JSON'
            }), 400

        user_id = data.get('userId')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Missing userId',
                'code': 'MISSING_USER_ID'
            }), 400

        # Query user's trip history, ordered by most recent first
        history_records = TripHistory.query.filter_by(user_id=user_id)\
                                          .order_by(TripHistory.timestamp.desc())\
                                          .all()

        # Convert to the expected format
        history_list = [record.to_dict() for record in history_records]

        return jsonify({
            'success': True,
            'data': {
                'history': history_list
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in /trip-history endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve trip history: {str(e)}',
            'code': 'SERVER_ERROR'
        }), 500


@trip_history_bp.route('/trip-history/save', methods=['POST'])
@track_api_hit
def save_trip_history():
    """Save a trip plan to user's history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON',
                'code': 'INVALID_JSON'
            }), 400

        # Validate required fields
        required_fields = ['userId', 'request', 'response', 'timestamp']
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'code': 'MISSING_FIELDS'
            }), 400

        # Extract data
        user_id = data.get('userId')
        request_data = data.get('request')
        response_data = data.get('response')
        timestamp_str = data.get('timestamp')

        # Parse timestamp
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid timestamp format. Expected ISO 8601 format.',
                'code': 'INVALID_TIMESTAMP'
            }), 400

        # Generate unique ID
        history_id = str(uuid.uuid4())

        # Create new trip history record
        new_trip = TripHistory(
            id=history_id,
            user_id=user_id,
            request_data=request_data,
            response_data=response_data,
            timestamp=timestamp,
            created_at=datetime.utcnow()
        )

        # Save to database
        db.session.add(new_trip)
        db.session.commit()

        logger.info(f"Trip plan saved successfully for user: {user_id}, id: {history_id}")

        return jsonify({
            'success': True,
            'message': 'Trip plan saved successfully',
            'data': {
                'id': history_id
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in /trip-history/save endpoint: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to save trip to history: {str(e)}',
            'code': 'SERVER_ERROR'
        }), 500


@trip_history_bp.route('/save-travel-plan', methods=['POST'])
@track_api_hit
def save_travel_plan():
    """Save generated travel plan to user's history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400

        # Validate required fields - updated to match frontend
        required_fields = ['userId', 'destination', 'travelPlan']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Extract data - updated to match frontend
        user_id = data.get('userId')  # Frontend sends userId instead of email
        destination = data.get('destination')
        preferences = data.get('preferences', '')
        budget = data.get('budget', '')
        language = data.get('language', 'english')
        travel_plan = data.get('travelPlan')

        # Create request object (what user requested)
        request_data = {
            'userId': user_id,
            'destination': destination,
            'preferences': preferences,
            'budget': budget,
            'language': language
        }

        # Response data is the travel plan
        response_data = travel_plan

        # Generate unique ID and timestamp
        history_id = str(uuid.uuid4())
        current_timestamp = datetime.utcnow()

        # Create new trip history record
        new_trip = TripHistory(
            id=history_id,
            user_id=user_id,  # Using userId as user identifier
            request_data=request_data,
            response_data=response_data,
            timestamp=current_timestamp,
            created_at=current_timestamp
        )

        # Save to database
        db.session.add(new_trip)
        db.session.commit()

        logger.info(f"Travel plan saved successfully for user: {user_id}, destination: {destination}, id: {history_id}")

        return jsonify({
            'success': True,
            'data': {
                'id': history_id,
                'message': 'Travel plan saved successfully'
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in /save-travel-plan endpoint: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to save travel plan: {str(e)}'
        }), 500 
