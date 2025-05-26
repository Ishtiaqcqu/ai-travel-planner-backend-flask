import google.generativeai as genai

class GeminiClient:
    """A utility class for interacting with Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.api_key = None
        self.model = None
    
    def initialize(self):
        """Initialize the client with the API key."""
        if not self.api_key:
            raise ValueError("Gemini API key not configured")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_response(self, prompt):
        """Generate a response using Gemini API.
        
        Args:
            prompt (str): The text prompt to send to Gemini
            
        Returns:
            str: The generated response text
        """
        if not self.model:
            self.initialize()
        
        response = self.model.generate_content(prompt)
        return response.text 