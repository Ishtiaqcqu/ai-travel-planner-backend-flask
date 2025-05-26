import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    logger.info(f"Starting server on port {os.environ.get('PORT', 5000)}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 