"""
Simple Test Cases for Ticket 2: Authentication
Run: python test_ticket_2.py
(Make sure server is running: python manage.py runserver)
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("\n" + "="*50)
print("TICKET 2 - AUTHENTICATION TESTS")
print("="*50)

# Test 1: Register User
print("\n✓ Test 1: User Registration")
try:
    response = requests.post(f"{BASE_URL}/auth/register/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "pass123"
    })
    if response.status_code == 201:
        token = response.json()['token']
        print(f"  ✅ PASS - User registered, Token: {token[:20]}...")
    elif response.status_code == 400:
        print(f"  ⚠️  User exists, trying login...")
        token = None
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
        token = None
except Exception as e:
    print(f"  ❌ FAIL - {e}")
    token = None

# Test 2: Login User
print("\n✓ Test 2: User Login")
try:
    response = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": "testuser",
        "password": "pass123"
    })
    if response.status_code == 200:
        token = response.json()['token']
        print(f"  ✅ PASS - Login successful, Token: {token[:20]}...")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

# Test 3: Access Protected Endpoint
print("\n✓ Test 3: Protected Endpoint (with token)")
try:
    response = requests.get(f"{BASE_URL}/activities/", 
                           headers={"Authorization": f"Token {token}"})
    if response.status_code == 200:
        print(f"  ✅ PASS - Accessed with authentication")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

# Test 4: Logout User
print("\n✓ Test 4: User Logout")
try:
    response = requests.post(f"{BASE_URL}/auth/logout/",
                            headers={"Authorization": f"Token {token}"})
    if response.status_code == 200:
        print(f"  ✅ PASS - Logout successful")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

print("\n" + "="*50)
print("TICKET 2 COMPLETE!")
print("="*50 + "\n")