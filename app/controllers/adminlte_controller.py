from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import db
from app.models.user import User
from app.models.admin import Admin
from app.models.app_config import AppConfig
from app.utils.admin_auth import login_required, login_admin, logout_admin, get_current_admin, is_admin_logged_in
from app.utils.api_tracker import get_api_stats
from sqlalchemy import func
import os

# Create the admin blueprint
adminlte_bp = Blueprint('adminlte', __name__)

@adminlte_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if is_admin_logged_in():
        return redirect(url_for('adminlte.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, admin = login_admin(username, password)
        if success:
            flash('Login successful!', 'success')
            return redirect(url_for('adminlte.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('adminlte/login.html')

@adminlte_bp.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_admin()
    flash('You have been logged out.', 'info')
    return redirect(url_for('adminlte.login'))

@adminlte_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Main admin dashboard"""
    # Get statistics
    total_users = User.query.count()
    api_stats = get_api_stats()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Get current Gemini API key status
    gemini_key = AppConfig.get_config('GEMINI_API_KEY', os.environ.get('GEMINI_API_KEY', ''))
    gemini_key_status = 'Configured' if gemini_key else 'Not Configured'
    
    return render_template('adminlte/dashboard.html', 
                         total_users=total_users,
                         api_stats=api_stats,
                         recent_users=recent_users,
                         gemini_key_status=gemini_key_status,
                         current_admin=get_current_admin())

@adminlte_bp.route('/users', methods=['GET'])
@login_required
def users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('adminlte/users.html', users=users)

@adminlte_bp.route('/api-stats', methods=['GET'])
@login_required
def api_stats():
    """API statistics page"""
    stats = get_api_stats()
    return render_template('adminlte/api_stats.html', stats=stats)

@adminlte_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Settings page for API key management"""
    if request.method == 'POST':
        gemini_api_key = request.form.get('gemini_api_key')
        
        if gemini_api_key:
            AppConfig.set_config(
                'GEMINI_API_KEY', 
                gemini_api_key, 
                'Gemini API Key for AI services',
                get_current_admin().id
            )
            flash('Gemini API key updated successfully!', 'success')
        else:
            flash('Please provide a valid API key.', 'error')
        
        return redirect(url_for('adminlte.settings'))
    
    # Get current settings
    gemini_key = AppConfig.get_config('GEMINI_API_KEY', '')
    
    return render_template('adminlte/settings.html', 
                         gemini_key=gemini_key,
                         current_admin=get_current_admin())

@adminlte_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change admin password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        admin = get_current_admin()
        
        if not admin.check_password(current_password):
            flash('Current password is incorrect.', 'error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'error')
        elif len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'error')
        else:
            admin.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('adminlte.dashboard'))
    
    return render_template('adminlte/change_password.html', current_admin=get_current_admin())

# API endpoints for AJAX requests
@adminlte_bp.route('/api/users', methods=['GET'])
@login_required
def api_users():
    """API endpoint to get users data"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@adminlte_bp.route('/api/stats', methods=['GET'])
@login_required
def api_dashboard_stats():
    """API endpoint to get dashboard statistics"""
    stats = get_api_stats()
    stats['total_users'] = User.query.count()
    return jsonify(stats)

# Legacy routes for backward compatibility
@adminlte_bp.route('/blank', methods=['GET'])
@login_required
def blank():
    """Route for displaying a blank AdminLTE page"""
    return render_template('adminlte/blank.html')

@adminlte_bp.route('/tables', methods=['GET'])
@login_required
def tables():
    """Route for displaying the tables page"""
    return render_template('adminlte/tables.html')

@adminlte_bp.route('/forms', methods=['GET'])
@login_required
def forms():
    """Route for displaying the forms page"""
    return render_template('adminlte/forms.html') 