import firebase_admin
from firebase_admin import credentials, auth
import logging
import os
from flask import current_app

logger = logging.getLogger(__name__)

# Path to your Firebase service account key JSON file
# Make sure to set FIREBASE_SERVICE_ACCOUNT_KEY in your environment variables
# or Flask app config.
SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY')

def initialize_firebase_app():
    """
    Initializes the Firebase Admin SDK if it hasn't been initialized yet.
    Relies on the FIREBASE_SERVICE_ACCOUNT_KEY environment variable
    or a 'FIREBASE_SERVICE_ACCOUNT_KEY' in Flask app.config pointing to the service account JSON.
    """
    if not firebase_admin._apps:
        try:
            # Try to get path from Flask app config first, then environment variable
            sa_key_path = current_app.config.get('FIREBASE_SERVICE_ACCOUNT_KEY', SERVICE_ACCOUNT_KEY_PATH)
            
            if not sa_key_path:
                logger.error("Firebase service account key path not found. "
                             "Set FIREBASE_SERVICE_ACCOUNT_KEY in config or environment.")
                return False

            if not os.path.exists(sa_key_path):
                logger.error(f"Firebase service account key file not found at path: {sa_key_path}")
                return False

            cred = credentials.Certificate(sa_key_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully.")
            return True
        except Exception as e:
            logger.error(f"Error initializing Firebase Admin SDK: {e}")
            return False
    return True # Already initialized

def verify_firebase_token(id_token):
    """
    Verifies a Firebase ID token.
    Returns the decoded token if valid, otherwise None.
    """
    if not initialize_firebase_app():
        return None
        
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except firebase_admin.auth.ExpiredIdTokenError:
        logger.warning("Firebase ID token has expired.")
        return None
    except firebase_admin.auth.InvalidIdTokenError:
        logger.warning("Firebase ID token is invalid.")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during token verification: {e}")
        return None

class FirebaseAuth:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initializes Firebase using Flask app configuration."""
        self.service_account_key_path = app.config.get('FIREBASE_SERVICE_ACCOUNT_KEY')
        if not self.service_account_key_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY not set in Flask app config.")
        
        if not os.path.exists(self.service_account_key_path):
             raise FileNotFoundError(f"Firebase service account key file not found at path: {self.service_account_key_path}")

        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(self.service_account_key_path)
                firebase_admin.initialize_app(cred)
                app.logger.info("Firebase Admin SDK initialized successfully via Flask extension.")
            except Exception as e:
                app.logger.error(f"Error initializing Firebase Admin SDK via Flask extension: {e}")
                raise
        # Store a reference to the app if needed, or handle initialization directly
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['firebase_auth'] = self


    def verify_id_token(self, id_token):
        """
        Verifies a Firebase ID token.
        Returns the decoded token if valid, otherwise None.
        """
        if not firebase_admin._apps:
            # This case should ideally be handled by init_app or a check before calling
            logger.error("Firebase app not initialized. Call init_app first or ensure it was initialized.")
            # Attempt re-initialization if a path is available (though this is not ideal for request handling)
            if self.service_account_key_path and os.path.exists(self.service_account_key_path):
                 cred = credentials.Certificate(self.service_account_key_path)
                 firebase_admin.initialize_app(cred)
                 logger.info("Firebase Admin SDK late initialized.")
            else:
                return None

        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except firebase_admin.auth.ExpiredIdTokenError:
            logger.warning("Firebase ID token has expired.")
            return None
        except firebase_admin.auth.InvalidIdTokenError:
            logger.warning("Firebase ID token is invalid.")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during token verification: {e}")
            return None

# Global instance for simple usage, can be initialized later with app context
# For more robust Flask integration, usually one would initialize this in create_app
firebase_auth_global = FirebaseAuth()

# Helper function for direct use, similar to before but using the class instance
def verify_token_globally(id_token):
    if not firebase_admin._apps:
        # Attempt to initialize if service account key is available via current_app or os.environ
        # This makes the global function more resilient if not using the Flask extension pattern
        initialize_firebase_app() 
    
    if not firebase_admin._apps:
        logger.error("Firebase not initialized for global verifier.")
        return None
        
    return firebase_auth_global.verify_id_token(id_token) 