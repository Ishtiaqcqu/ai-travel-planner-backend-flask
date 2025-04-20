# Flask Backend with Gemini API and PostgreSQL

A Flask-based backend application that integrates with Google's Gemini API and PostgreSQL database.

## Features

- Flask REST API framework
- PostgreSQL database integration with SQLAlchemy
- Google Gemini API integration
- Environment-based configuration

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file based on the `.env.example` template
6. Add your PostgreSQL and Gemini API credentials to the `.env` file

## Database Initialization

Initialize the database with the following commands:

```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

Start the application with:

```
flask run
```

Or for development with auto-reload:

```
flask --debug run
```

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /api/test-db`: Test PostgreSQL database connection
- `GET /api/test-gemini`: Test Gemini API connection

## Development

Additional endpoints and functionality will be added as needed. 