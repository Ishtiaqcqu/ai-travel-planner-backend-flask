#!/usr/bin/env python3
"""
Setup script for admin panel
Creates database tables and default admin user
"""

import os
import sys
from app import create_app
from app.models import db
from app.utils.admin_auth import create_default_admin

def setup_admin():
    """Setup admin panel with default admin user"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all database tables
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Create default admin user
            print("Creating default admin user...")
            admin = create_default_admin()
            
            if admin:
                print("✓ Default admin user created successfully")
                print("  Username: admin")
                print("  Password: admin123")
                print("  ⚠️  IMPORTANT: Please change the default password after first login!")
            else:
                print("ℹ️  Admin user already exists")
            
            print("\n🎉 Admin panel setup completed!")
            print("You can now access the admin panel at: http://localhost:5000/admin/login")
            
        except Exception as e:
            print(f"❌ Error during setup: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    setup_admin() 