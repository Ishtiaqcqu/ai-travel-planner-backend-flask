from flask import Blueprint, jsonify, request
import logging
import uuid
from datetime import datetime
from app.models import db
from app.models.translation_history import TranslationHistory
from app.utils.api_tracker import track_api_hit

logger = logging.getLogger(__name__)

translation_history_bp = Blueprint('translation_history', __name__)

@translation_history_bp.route('/translation-history', methods=['POST'])
@track_api_hit
def get_translation_history():
    """Retrieve user's translation history."""
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

        # Query user's translation history, ordered by most recent first
        history_records = TranslationHistory.query.filter_by(user_id=user_id)\
                                                 .order_by(TranslationHistory.timestamp.desc())\
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
        logger.error(f"Error in /translation-history endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve translation history: {str(e)}',
            'code': 'SERVER_ERROR'
        }), 500


@translation_history_bp.route('/translation-history/save', methods=['POST'])
@track_api_hit
def save_translation_history():
    """Save a new translation to user's history."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON',
                'code': 'INVALID_JSON'
            }), 400

        # Validate required fields
        required_fields = [
            'userId', 'sourceText', 'translatedText', 'sourceLanguage', 
            'targetLanguage', 'sourceLanguageLabel', 'targetLanguageLabel', 'timestamp'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'code': 'MISSING_FIELDS'
            }), 400

        # Extract data
        user_id = data.get('userId')
        source_text = data.get('sourceText')
        translated_text = data.get('translatedText')
        source_language = data.get('sourceLanguage')
        target_language = data.get('targetLanguage')
        source_language_label = data.get('sourceLanguageLabel')
        target_language_label = data.get('targetLanguageLabel')
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

        # Create new translation history record
        new_translation = TranslationHistory(
            id=history_id,
            user_id=user_id,
            source_text=source_text,
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
            source_language_label=source_language_label,
            target_language_label=target_language_label,
            timestamp=timestamp,
            created_at=datetime.utcnow()
        )

        # Save to database
        db.session.add(new_translation)
        db.session.commit()

        logger.info(f"Translation saved successfully for user: {user_id}, id: {history_id}")

        return jsonify({
            'success': True,
            'message': 'Translation saved successfully',
            'data': {
                'id': history_id
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in /translation-history/save endpoint: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to save translation to history: {str(e)}',
            'code': 'SERVER_ERROR'
        }), 500 