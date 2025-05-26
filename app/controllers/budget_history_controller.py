from flask import Blueprint, jsonify, request
import logging
import uuid
from datetime import datetime
from app.models import db
from app.models.budget_history import BudgetHistory
from app.utils.api_tracker import track_api_hit

logger = logging.getLogger(__name__)

budget_history_bp = Blueprint('budget_history', __name__)

@budget_history_bp.route('/budget-history', methods=['POST'])
@track_api_hit
def get_budget_history():
    """Retrieve user's budget planning history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be JSON', 'message': 'Request body must be JSON'}), 400

        user_id = data.get('userId')
        if not user_id:
            return jsonify({'error': 'Missing userId', 'message': 'Missing userId'}), 400

        # Query user's budget history, ordered by most recent first
        history_records = BudgetHistory.query.filter_by(user_id=user_id)\
                                           .order_by(BudgetHistory.created_at.desc())\
                                           .all()

        # Convert to the expected format
        history_list = [record.to_dict() for record in history_records]

        return jsonify({
            'history': history_list
        }), 200

    except Exception as e:
        logger.error(f"Error in /budget-history endpoint: {str(e)}")
        return jsonify({
            'error': f'Failed to retrieve budget history: {str(e)}',
            'message': f'Failed to retrieve budget history: {str(e)}'
        }), 500


@budget_history_bp.route('/budget-history/save', methods=['POST'])
@track_api_hit
def save_budget_history():
    """Save a budget plan to user's history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body must be JSON'}), 400

        # Validate required fields
        user_id = data.get('userId')
        request_data = data.get('request')
        response_data = data.get('response')

        if not user_id:
            return jsonify({'success': False, 'error': 'Missing userId'}), 400
        if not request_data:
            return jsonify({'success': False, 'error': 'Missing request data'}), 400
        if not response_data:
            return jsonify({'success': False, 'error': 'Missing response data'}), 400

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

        # Create new budget history record
        new_history = BudgetHistory(
            id=history_id,
            user_id=user_id,
            request_data=request_data,
            response_data=response_data,
            created_at=created_at
        )

        # Save to database
        db.session.add(new_history)
        db.session.commit()

        logger.info(f"Budget history saved successfully for user: {user_id}, id: {history_id}")

        return jsonify({
            'success': True,
            'id': history_id
        }), 201

    except Exception as e:
        logger.error(f"Error in /budget-history/save endpoint: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to save budget to history: {str(e)}'
        }), 500 