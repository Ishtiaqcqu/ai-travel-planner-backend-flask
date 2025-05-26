from flask import Blueprint, request, jsonify
import logging
import json
from app.utils.api_tracker import track_api_hit
from app.utils.gemini_client import GeminiClient
from flask import current_app

logger = logging.getLogger(__name__)

travel_plan_bp = Blueprint('travel_plan', __name__)

@travel_plan_bp.route('/generate-travel-plan', methods=['POST'])
@track_api_hit
def generate_travel_plan():
    """Generate AI-powered travel plan using Gemini API."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400

        # Extract required fields
        destination = data.get('destination')
        preferences = data.get('preferences', '')
        budget = data.get('budget', 'medium')
        language = data.get('language', 'english')
        user_id = data.get('userId', '')

        # Validate required fields
        if not destination:
            return jsonify({
                'success': False,
                'error': 'Destination is required'
            }), 400

        logger.info(f"Generating travel plan for destination: {destination}, budget: {budget}, language: {language}")

        # Check if Gemini API is configured
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            logger.warning("Gemini API key not configured, returning mock data")
            return _get_mock_travel_plan(destination, budget, language)

        # Create detailed prompt for AI
        prompt = _create_travel_plan_prompt(destination, preferences, budget, language)
        
        try:
            # Initialize Gemini client and generate response
            gemini_client = GeminiClient()
            gemini_client.api_key = api_key
            ai_response = gemini_client.generate_response(prompt)
            
            # Parse AI response into structured format
            travel_plan = _parse_ai_response(ai_response, destination, budget)
            
            return jsonify({
                'success': True,
                'data': travel_plan
            }), 200
            
        except Exception as ai_error:
            logger.error(f"AI generation failed: {str(ai_error)}, falling back to mock data")
            return _get_mock_travel_plan(destination, budget, language)

    except Exception as e:
        logger.error(f"Error in /generate-travel-plan endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to generate travel plan: {str(e)}'
        }), 500


def _create_travel_plan_prompt(destination, preferences, budget, language):
    """Create a detailed prompt for AI travel plan generation."""
    budget_descriptions = {
        'low': 'budget-friendly, economical options',
        'medium': 'mid-range, good value options',
        'high': 'luxury, premium options'
    }
    
    budget_desc = budget_descriptions.get(budget.lower(), 'mid-range')
    
    prompt = f"""
    Create a comprehensive travel plan for {destination} with the following requirements:
    - Budget level: {budget_desc}
    - Preferences: {preferences}
    - Language: {language}
    
    Please provide recommendations in the following categories and format your response as JSON:
    
    {{
        "accommodation": ["list of 3-5 accommodation recommendations"],
        "food": ["list of 3-5 food and dining recommendations"],
        "attractions": ["list of 5-7 tourist attractions and activities"],
        "transportation": ["list of 3-4 transportation options"],
        "safetyTips": ["list of 4-5 safety tips specific to the destination"],
        "budgetAdvice": ["list of 3-4 budget management tips"],
        "images": ["list of 3-5 relevant image search terms for the destination"]
    }}
    
    Make sure all recommendations are specific to {destination} and appropriate for the {budget_desc} budget level.
    Provide practical, actionable advice that travelers can actually use.
    """
    
    return prompt


def _parse_ai_response(ai_response, destination, budget):
    """Parse AI response into structured travel plan format."""
    try:
        # Try to parse as JSON first
        if isinstance(ai_response, str):
            # Look for JSON content in the response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = ai_response[start_idx:end_idx]
                parsed_data = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['accommodation', 'food', 'attractions', 'transportation', 'safetyTips', 'budgetAdvice']
                for field in required_fields:
                    if field not in parsed_data:
                        parsed_data[field] = []
                
                # Add images if not present
                if 'images' not in parsed_data:
                    parsed_data['images'] = [
                        f"{destination} landmarks",
                        f"{destination} attractions",
                        f"{destination} food",
                        f"{destination} culture",
                        f"{destination} scenery"
                    ]
                
                return parsed_data
        
        # If JSON parsing fails, fall back to mock data
        logger.warning("Failed to parse AI response as JSON, using mock data")
        return _get_mock_travel_plan_data(destination, budget)
        
    except Exception as e:
        logger.error(f"Error parsing AI response: {str(e)}")
        return _get_mock_travel_plan_data(destination, budget)


def _get_mock_travel_plan(destination, budget, language):
    """Return mock travel plan data when AI is not available."""
    travel_plan = _get_mock_travel_plan_data(destination, budget)
    
    return jsonify({
        'success': True,
        'data': travel_plan
    }), 200


def _get_mock_travel_plan_data(destination, budget):
    """Generate mock travel plan data."""
    budget_modifiers = {
        'low': 'budget-friendly',
        'medium': 'mid-range',
        'high': 'luxury'
    }
    
    modifier = budget_modifiers.get(budget.lower(), 'mid-range')
    
    return {
        "accommodation": [
            f"{modifier.title()} hotels in {destination}",
            f"Recommended {modifier} guesthouses",
            f"Popular {modifier} accommodations",
            f"Well-rated {modifier} lodging options"
        ],
        "food": [
            f"Traditional {destination} cuisine restaurants",
            f"Popular local food markets",
            f"Recommended {modifier} dining spots",
            f"Must-try local dishes in {destination}"
        ],
        "attractions": [
            f"Top landmarks in {destination}",
            f"Historical sites and museums",
            f"Natural attractions and parks",
            f"Cultural experiences",
            f"Popular tourist activities",
            f"Local markets and shopping areas"
        ],
        "transportation": [
            f"Public transportation in {destination}",
            f"Taxi and ride-sharing options",
            f"Car rental recommendations",
            f"Walking and cycling routes"
        ],
        "safetyTips": [
            f"General safety guidelines for {destination}",
            "Keep important documents secure",
            "Stay aware of your surroundings",
            "Use reputable transportation services",
            "Follow local customs and laws"
        ],
        "budgetAdvice": [
            f"Cost-effective ways to explore {destination}",
            f"Money-saving tips for {modifier} travelers",
            "Best times to visit for lower costs",
            "Free or low-cost activities"
        ],
        "images": [
            f"{destination} landmarks",
            f"{destination} attractions",
            f"{destination} food",
            f"{destination} culture",
            f"{destination} scenery"
        ]
    } 