#!/usr/bin/env python3
"""
Quick Setup Script for Capstone Backend
Automates the setup process for new machines
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Please upgrade Python.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_postgresql():
    """Check if PostgreSQL is available"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  PostgreSQL not found in PATH. Please ensure PostgreSQL is installed and accessible.")
    return False

def create_env_file():
    """Create .env file with template"""
    env_content = """# Database Configuration
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=your_database_name

# Flask Configuration
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
FLASK_ENV=development
FLASK_APP=run.py

# API Keys (Optional)
GEMINI_API_KEY=your-gemini-api-key-if-you-have-one

# Firebase Configuration (if using Firebase)
FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("⚠️  Please edit .env file with your actual database credentials!")
        return True
    else:
        print("ℹ️  .env file already exists")
        return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    if not os.path.exists('venv'):
        if not run_command('python -m venv venv', 'Creating virtual environment'):
            return False
    
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Already in virtual environment")
        return True
    
    print("ℹ️  Virtual environment created. Please activate it:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    # Try to install from requirements.txt first
    if os.path.exists('requirements.txt'):
        if run_command('pip install -r requirements.txt', 'Installing dependencies from requirements.txt'):
            return True
    
    # Fallback to individual packages
    packages = [
        'flask',
        'flask-cors',
        'flask-sqlalchemy',
        'flask-migrate',
        'psycopg2-binary',
        'python-dotenv',
        'google-generativeai',
        'firebase-admin',
        'werkzeug'
    ]
    
    for package in packages:
        if not run_command(f'pip install {package}', f'Installing {package}'):
            print(f"⚠️  Failed to install {package}, continuing...")
    
    return True

def main():
    """Main setup function"""
    print("🚀 Capstone Backend Quick Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    check_postgresql()  # Warning only, not blocking
    
    # Setup steps
    steps = [
        (setup_virtual_environment, "Setting up virtual environment"),
        (install_dependencies, "Installing dependencies"),
        (create_env_file, "Creating environment file"),
    ]
    
    for step_func, description in steps:
        print(f"\n📋 {description}")
        if not step_func():
            print(f"❌ Setup failed at: {description}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Quick setup completed!")
    print("\n📝 Next steps:")
    print("1. Edit .env file with your database credentials")
    print("2. Create PostgreSQL database and user")
    print("3. Activate virtual environment (if not already active)")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("4. Run: python setup_admin.py")
    print("5. Run: python run.py")
    print("6. Access admin panel: http://localhost:5000/admin/login")
    print("   Default credentials: admin / admin123")
    print("\n📖 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main() 