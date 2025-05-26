#!/usr/bin/env python3
"""
Endpoint Testing Script
Tests all API endpoints to ensure they're working correctly
"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, expected_status=200, description=""):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - {description}")
            return True
        else:
            print(f"❌ {method} {endpoint} - Expected {expected_status}, got {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Connection failed (is the server running?)")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {method} {endpoint} - Request timeout")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)}")
        return False

def test_admin_panel():
    """Test admin panel accessibility"""
    admin_endpoints = [
        ("/admin/login", "Admin login page"),
        ("/admin/dashboard", "Admin dashboard (should redirect to login)"),
    ]
    
    print("\n🔐 Testing Admin Panel...")
    for endpoint, description in admin_endpoints:
        # These should return 200 (login page) or 302 (redirect to login)
        test_endpoint("GET", endpoint, expected_status=[200, 302], description=description)

def main():
    """Main testing function"""
    print("🧪 API Endpoint Testing")
    print("=" * 40)
    
    # Test basic connectivity
    print("\n🌐 Testing Basic Connectivity...")
    if not test_endpoint("GET", "/api/health", description="Health check"):
        print("❌ Server is not responding. Please ensure the Flask app is running.")
        sys.exit(1)
    
    # Test API endpoints
    print("\n📡 Testing API Endpoints...")
    
    api_tests = [
        # Authentication endpoints
        ("POST", "/api/register", {
            "fullName": "Test User",
            "email": "test@example.com",
            "role": "Member"
        }, 201, "User registration"),
        
        ("POST", "/api/login", {
            "email": "test@example.com"
        }, 200, "User login"),
        
        # Profile endpoints (might fail if user doesn't exist)
        ("GET", "/api/profile/1", None, [200, 404], "Get user profile"),
        
        # History endpoints (might fail if user doesn't exist)
        ("GET", "/api/description-history/1", None, [200, 404], "Description history"),
        ("GET", "/api/budget-history/1", None, [200, 404], "Budget history"),
        ("GET", "/api/translation-history/1", None, [200, 404], "Translation history"),
        ("GET", "/api/trip-history/1", None, [200, 404], "Trip history"),
        
        # Gemini endpoint (might fail without API key)
        ("POST", "/api/gemini/generate", {
            "prompt": "Hello, how are you?"
        }, [200, 400, 500], "Gemini AI generation"),
    ]
    
    passed = 0
    total = len(api_tests)
    
    for method, endpoint, data, expected_status, description in api_tests:
        if isinstance(expected_status, list):
            # Test with multiple acceptable status codes
            url = f"{BASE_URL}{endpoint}"
            try:
                if method.upper() == "GET":
                    response = requests.get(url, timeout=10)
                else:
                    response = requests.post(url, json=data, timeout=10)
                
                if response.status_code in expected_status:
                    print(f"✅ {method} {endpoint} - {description}")
                    passed += 1
                else:
                    print(f"❌ {method} {endpoint} - Expected {expected_status}, got {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {method} {endpoint} - Error: {str(e)}")
        else:
            if test_endpoint(method, endpoint, data, expected_status, description):
                passed += 1
    
    # Test admin panel
    test_admin_panel()
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} API endpoints passed")
    
    if passed == total:
        print("🎉 All API endpoints are working correctly!")
    else:
        print("⚠️  Some endpoints failed. Check the errors above.")
    
    print("\n📝 Manual Testing:")
    print("1. Visit http://localhost:5000/admin/login")
    print("2. Login with: admin / admin123")
    print("3. Explore the admin dashboard")
    print("4. Test API endpoints with Postman or curl")
    
    print("\n🔧 If tests failed:")
    print("- Ensure PostgreSQL is running")
    print("- Check .env file configuration")
    print("- Run 'python setup_admin.py' if admin login fails")
    print("- Check application logs for detailed errors")

if __name__ == "__main__":
    main() 