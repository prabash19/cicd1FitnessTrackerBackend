"""
Simple Test Cases for Ticket 3: Activity API
Run: python test_ticket_3.py
(Make sure server is running: python manage.py runserver)
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api"

# First login to get token
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "testuser",
    "password": "pass123"
})
token = response.json()['token']
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}

print("\n" + "="*50)
print("TICKET 3 - ACTIVITY API TESTS")
print("="*50)

# Test 1: Create Activity
print("\n✓ Test 1: Create Activity")
try:
    response = requests.post(f"{BASE_URL}/activities/", 
        headers=headers,
        json={
            "activity_type": "workout",
            "title": "Morning Run",
            "status": "planned",
            "duration_minutes": 30,
            "calories": 250,
            "date": "2024-11-08"
        })
    if response.status_code == 201:
        activity_id = response.json()['id']
        print(f"  ✅ PASS - Activity created, ID: {activity_id}")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
        activity_id = None
except Exception as e:
    print(f"  ❌ FAIL - {e}")
    activity_id = None

# Test 2: List Activities
print("\n✓ Test 2: List All Activities")
try:
    response = requests.get(f"{BASE_URL}/activities/", headers=headers)
    if response.status_code == 200:
        count = response.json()['count']
        print(f"  ✅ PASS - Found {count} activities")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

# Test 3: Update Activity Status
print("\n✓ Test 3: Update Activity Status")
try:
    if activity_id:
        response = requests.patch(f"{BASE_URL}/activities/{activity_id}/",
            headers=headers,
            json={"status": "completed"})
        if response.status_code == 200:
            print(f"  ✅ PASS - Status updated to completed")
        else:
            print(f"  ❌ FAIL - Status: {response.status_code}")
    else:
        print(f"  ⚠️  SKIP - No activity to update")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

# Test 4: Delete Activity
print("\n✓ Test 4: Delete Activity")
try:
    if activity_id:
        response = requests.delete(f"{BASE_URL}/activities/{activity_id}/",
                                  headers=headers)
        if response.status_code == 204:
            print(f"  ✅ PASS - Activity deleted")
        else:
            print(f"  ❌ FAIL - Status: {response.status_code}")
    else:
        print(f"  ⚠️  SKIP - No activity to delete")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

print("\n" + "="*50)
print("TICKET 3 COMPLETE!")
print("="*50 + "\n")