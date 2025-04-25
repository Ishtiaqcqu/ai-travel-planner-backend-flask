from flask import Blueprint, jsonify, current_app
import logging
from app.utils.gemini_client import GeminiClient

logger = logging.getLogger(__name__)
gemini_client = GeminiClient()

gemini_bp = Blueprint('gemini', __name__)

@gemini_bp.route('/test-gemini', methods=['GET'])
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
        gemini_client.api_key = api_key
        response = gemini_client.generate_response("Hello, this is a test.")
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully connected to Gemini API',
            'test_response': response
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to connect to Gemini API: {str(e)}'
        }), 500 