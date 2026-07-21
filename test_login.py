"""
Test Login Endpoint

This script tests the login endpoint with the correct OAuth2 form format.
"""

import requests

def test_login():
    print("=" * 70)
    print("Testing Login Endpoint")
    print("=" * 70)
    print()
    
    # The login endpoint expects form data, not JSON
    url = "http://127.0.0.1:8000/api/v1/auth/login"
    
    # OAuth2PasswordRequestForm expects form data (application/x-www-form-urlencoded)
    data = {
        "username": "admin",
        "password": "Admin123!"
    }
    
    print(f"POST {url}")
    print(f"Form Data: {data}")
    print()
    
    try:
        response = requests.post(url, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
        if response.status_code == 200:
            print("SUCCESS: Login works!")
            token_data = response.json()
            print(f"Access Token: {token_data.get('access_token', '')[:50]}...")
            print(f"Token Type: {token_data.get('token_type')}")
        else:
            print("FAILED: Login returned HTTP {response.status_code}")
            
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("=" * 70)

if __name__ == "__main__":
    test_login()
