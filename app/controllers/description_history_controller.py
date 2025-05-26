from flask import Blueprint, jsonify, request
import logging
import uuid
from datetime import datetime
from app.models import db
from app.models.description_history import DescriptionHistory
from app.utils.api_tracker import track_api_hit

logger = logging.getLogger(__name__)

history_bp = Blueprint('history', __name__)

@history_bp.route('/history-description', methods=['POST'])
@track_api_hit
def get_description_history():
    """Retrieve user's destination description history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

        user_id = data.get('userId')
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Missing userId'}), 400

        # Query user's description history, ordered by most recent first
        history_records = DescriptionHistory.query.filter_by(user_id=user_id)\
                                                 .order_by(DescriptionHistory.created_at.desc())\
                                                 .all()

        # Convert to the expected format
        history_list = [record.to_dict() for record in history_records]

        return jsonify({
            'history': history_list
        }), 200

    except Exception as e:
        logger.error(f"Error in /history-description endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to retrieve description history: {str(e)}'
        }), 500


@history_bp.route('/history-description/save', methods=['POST'])
@track_api_hit
def save_description_history():
    """Save a destination description to user's history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

        # Validate required fields
        user_id = data.get('userId')
        request_data = data.get('request')
        response_data = data.get('response')

        if not user_id:
            return jsonify({'status': 'error', 'message': 'Missing userId'}), 400
        if not request_data:
            return jsonify({'status': 'error', 'message': 'Missing request data'}), 400
        if not response_data:
            return jsonify({'status': 'error', 'message': 'Missing response data'}), 400

        # Generate unique ID
        history_id = str(uuid.uuid4())

        # Parse createdAt or use current time
        created_at_str = data.get('createdAt')
        if created_at_str:
            try:
                created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
            except ValueError:
                created_at = datetime.utcnow()
        else:
            created_at = datetime.utcnow()

        # Create new history record
        new_history = DescriptionHistory(
            id=history_id,
            user_id=user_id,
            request_data=request_data,
            response_data=response_data,
            created_at=created_at
        )

        # Save to database
        db.session.add(new_history)
        db.session.commit()

        logger.info(f"Description history saved successfully for user: {user_id}, id: {history_id}")

        return jsonify({
            'status': 'success',
            'message': 'Description saved to history successfully',
            'id': history_id
        }), 201

    except Exception as e:
        logger.error(f"Error in /history-description/save endpoint: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to save description to history: {str(e)}'
        }), 500 