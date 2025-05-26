from flask import session, request, redirect, url_for, flash
from functools import wraps
from app.models.admin import Admin
from app.models import db
from datetime import datetime

def login_required(f):
    """Decorator to require admin login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('adminlte.login'))
        return f(*args, **kwargs)
    return decorated_function

def login_admin(username, password):
    """Authenticate admin and create session"""
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and admin.check_password(password):
        # Update last login
        admin.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create session
        session['admin_id'] = admin.id
        session['admin_username'] = admin.username
        session.permanent = True
        
        return True, admin
    
    return False, None

def logout_admin():
    """Clear admin session"""
    session.pop('admin_id', None)
    session.pop('admin_username', None)

def get_current_admin():
    """Get current logged in admin"""
    if 'admin_id' in session:
        return Admin.query.get(session['admin_id'])
    return None

def is_admin_logged_in():
    """Check if admin is logged in"""
    return 'admin_id' in session

def create_default_admin():
    """Create default admin if none exists"""
    if Admin.query.count() == 0:
        admin = Admin(username='admin')
        admin.set_password('admin123')  # Default password - should be changed
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: username='admin', password='admin123'")
        print("Please change the default password after first login!")
        return admin
    return None 