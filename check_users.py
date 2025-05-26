from app import create_app
from app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"Found {len(users)} users in the database:")
    print("-" * 50)
    
    if users:
        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.fullName}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Passport: {user.passport_number}")
            print(f"Travel Preferences: {user.travel_preferences}")
            print(f"Created: {user.created_at}")
            print("-" * 50)
    else:
        print("No users found in the database.")
        print("You may need to register a user first using the /api/register endpoint.") 