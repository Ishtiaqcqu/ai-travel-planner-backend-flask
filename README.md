# Capstone Backend

A Flask-based backend API built using the Model-View-Controller (MVC) architectural pattern.

## Project Structure

The project follows the MVC architectural pattern:

```
capstone-backend/
├── app/                    # Main application package
│   ├── models/             # Data models
│   │   ├── __init__.py     # Database setup
│   │   ├── user.py         # User model
│   │   └── example.py      # Example model
│   ├── controllers/        # Controllers/routes
│   │   ├── __init__.py
│   │   ├── auth_controller.py    # Authentication endpoints
│   │   ├── health_controller.py  # Health check endpoints
│   │   └── gemini_controller.py  # Gemini AI endpoints
│   ├── views/              # View templates (not heavily used in API)
│   │   └── __init__.py
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   ├── db_utils.py     # Database utilities
│   │   └── gemini_client.py # Gemini AI client
│   ├── config/             # Configuration
│   │   ├── __init__.py
│   │   └── config.py       # App configuration
│   └── __init__.py         # App factory
├── migrations/             # Database migrations
├── run.py                  # Application entry point
├── setup_db.py             # Database setup script
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## MVC Pattern Implementation

- **Models**: Located in `app/models/`, these files define the data structure and database schema.
- **Views**: In this API-focused application, views are the JSON responses returned by controllers.
- **Controllers**: Located in `app/controllers/`, these handle the request/response cycle and application logic.

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Environment Variables

Create a `.env` file with the following variables:

```
SECRET_KEY=your-secret-key
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_NAME=your-db-name
GEMINI_API_KEY=your-gemini-api-key
```

### Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python setup_db.py
   ```

5. Run the application:
   ```
   python run.py
   ```

## API Endpoints

- `/api/health` - Health check endpoint
- `/api/test-db` - Test database connection
- `/api/test-gemini` - Test Gemini AI connection
- `/api/register` - Register a new user
- `/api/verifylogin` - Verify user login

## Setup on a New PC (No Python)

### Install Python
```
# Download and run Python installer from https://www.python.org/downloads/
# During installation, check "Add Python to PATH"
python --version
```
```
Python 3.11.4
```

### Clone Repository
```
# Install Git from https://git-scm.com/downloads
git clone https://github.com/your-username/capstone-backend.git
cd capstone-backend
```
```
Cloning into 'capstone-backend'...
```

### Create Environment File
```
# Create .env file with your credentials
echo SECRET_KEY=your-secret-key > .env
echo DB_USER=your-db-username >> .env
echo DB_PASSWORD=your-db-password >> .env
echo DB_HOST=your-db-host >> .env
echo DB_NAME=your-db-name >> .env
echo GEMINI_API_KEY=your-gemini-api-key >> .env
```

### Create Virtual Environment
```
python -m venv venv
```

### Activate Virtual Environment
```
# Windows
venv\Scripts\activate
```
```
(venv) PS D:\capstone-backend>
```

### Install Dependencies
```
pip install -r requirements.txt
``
Collecting Flask==2.3.3
  Downloading Flask-2.3.3-py3-none-any.whl (96 kB)
...
Successfully installed Flask-2.3.3 Flask-Cors-4.0.0 Flask-Migrate-4.0.5 Flask-SQLAlchemy-3.1.1 ...
```

### Initialize Database
```
python setup_db.py
```
```
INFO:app.config.config:Environment variables loaded in config
INFO:app:Environment variables loaded
INFO:app:CORS initialized
INFO:app:Database initialized successfully
...
INFO:__main__:Database setup completed successfully
```

### Run Application
```
python run.py
```
```
INFO:app.config.config:Environment variables loaded in config
INFO:app:Environment variables loaded
INFO:app:CORS initialized
INFO:app:Database initialized successfully
INFO:app:API routes registered
INFO:__main__:Starting server on port 5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Access API at: http://127.0.0.1:5000/api/health 
