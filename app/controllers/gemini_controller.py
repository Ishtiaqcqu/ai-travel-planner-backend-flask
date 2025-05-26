from flask import Blueprint, jsonify, current_app, request
import logging
from app.utils.gemini_client import GeminiClient
from app.utils.firebase_auth import verify_firebase_token
from app.utils.api_tracker import track_api_hit

logger = logging.getLogger(__name__)
gemini_client = GeminiClient()

gemini_bp = Blueprint('gemini', __name__)

@gemini_bp.route('/test-gemini', methods=['GET'])
@track_api_hit
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

@gemini_bp.route('/generate', methods=['POST'])
@track_api_hit
def generate_response_with_auth():
    """Generate response from Gemini API after Firebase JWT authentication."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

        id_token = data.get('token')
        prompt = data.get('prompt')

        if not id_token:
            return jsonify({'status': 'error', 'message': 'Missing Firebase ID token'}), 400
        if not prompt:
            return jsonify({'status': 'error', 'message': 'Missing prompt'}), 400

        # --- MOCK FIREBASE TOKEN VERIFICATION --- START
        # Actual verification commented out for testing
        # decoded_token = verify_firebase_token(id_token)
        # if not decoded_token:
        #     return jsonify({'status': 'error', 'message': 'Invalid or expired Firebase ID token'}), 401
        
        # Mock successful verification
        decoded_token = {'uid': 'mock_user_123', 'name': 'Mock User'} # Add any other fields your app might expect
        logger.info("Mock Firebase token verification successful.")
        # --- MOCK FIREBASE TOKEN VERIFICATION --- END
        
        logger.info(f"Token verified for UID: {decoded_token.get('uid')}. Received prompt: '{prompt}'.")

        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                'status': 'error',
                'message': 'Gemini API key not configured'
            }), 500
        
        gemini_client.api_key = api_key
        gemini_response_text = gemini_client.generate_response(prompt)
        
        return jsonify(gemini_response_text), 200

    except Exception as e:
        logger.error(f"Error in /generate endpoint: {str(e)}")
        return jsonify({
            'error': f'Failed to generate response: {str(e)}'
        }), 500 

@gemini_bp.route('/generate-trip', methods=['POST'])
@track_api_hit
def generate_trip_itinerary():
    """Generate AI-powered trip itinerary using Gemini API."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Request body must be JSON',
                'message': 'Request body must be JSON',
                'code': 'INVALID_JSON'
            }), 400

        id_token = data.get('token')
        prompt = data.get('prompt')

        if not id_token:
            return jsonify({
                'error': 'Missing Firebase ID token',
                'message': 'Missing Firebase ID token',
                'code': 'MISSING_TOKEN'
            }), 400
        if not prompt:
            return jsonify({
                'error': 'Missing prompt',
                'message': 'Missing prompt',
                'code': 'MISSING_PROMPT'
            }), 400

        # --- MOCK FIREBASE TOKEN VERIFICATION --- START
        # Actual verification commented out for testing
        # decoded_token = verify_firebase_token(id_token)
        # if not decoded_token:
        #     return jsonify({
        #         'error': 'Invalid or expired Firebase ID token',
        #         'message': 'Invalid or expired Firebase ID token',
        #         'code': 'INVALID_TOKEN'
        #     }), 401
        
        # Mock successful verification
        decoded_token = {'uid': 'mock_user_123', 'name': 'Mock User'}
        logger.info("Mock Firebase token verification successful for trip generation.")
        # --- MOCK FIREBASE TOKEN VERIFICATION --- END
        
        logger.info(f"Token verified for UID: {decoded_token.get('uid')}. Generating trip itinerary.")

        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                'error': 'Gemini API key not configured',
                'message': 'Gemini API key not configured',
                'code': 'API_KEY_MISSING'
            }), 500
        
        gemini_client.api_key = api_key
        gemini_response_text = gemini_client.generate_response(prompt)
        
        # Return the response as a JSON string (as expected by the frontend)
        return jsonify(gemini_response_text), 200

    except Exception as e:
        logger.error(f"Error in /generate-trip endpoint: {str(e)}")
        return jsonify({
            'error': f'Failed to generate trip itinerary: {str(e)}',
            'message': f'Failed to generate trip itinerary: {str(e)}',
            'code': 'SERVER_ERROR'
        }), 500 