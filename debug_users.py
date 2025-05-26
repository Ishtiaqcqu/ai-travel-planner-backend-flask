from app import create_app
from app.models import db
from app.models.user import User
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    # Check table structure
    inspector = inspect(db.engine)
    columns = inspector.get_columns('users')
    
    print("=== USERS TABLE STRUCTURE ===")
    for column in columns:
        print(f"Column: {column['name']}, Type: {column['type']}, Nullable: {column['nullable']}")
    
    print("\n=== RAW SQL QUERY ===")
    # Raw SQL query to see all data
    result = db.session.execute(text("SELECT * FROM users"))
    rows = result.fetchall()
    
    print(f"Found {len(rows)} rows in users table:")
    for row in rows:
        print(f"Row: {dict(row._mapping)}")
    
    print("\n=== SQLALCHEMY QUERY ===")
    # SQLAlchemy query
    users = User.query.all()
    print(f"Found {len(users)} users via SQLAlchemy:")
    for user in users:
        print(f"User: {user.to_dict()}")
    
    print("\n=== DATABASE INFO ===")
    print(f"Database URL: {db.engine.url}")
    print(f"Current schema: {db.engine.dialect.default_schema_name}") 