import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from models import db, init_app
from routes import api

# Load environment variables
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    init_app(app)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Basic health check endpoint"""
        return jsonify({'status': 'ok', 'message': 'Service is running'})
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 