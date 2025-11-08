"""
Simple Test Cases for Ticket 1: Backend Setup
Run: python test_ticket_1.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_tracker.settings')
django.setup()

from django.db import connection
from django.conf import settings
from django.contrib.auth.models import User

print("\n" + "="*50)
print("TICKET 1 - BACKEND SETUP TESTS")
print("="*50)

# Test 1: Database Connection
print("\n✓ Test 1: Database Connection")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"  ✅ PASS - Connected to PostgreSQL")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

# Test 2: Check Installed Apps
print("\n✓ Test 2: Required Apps Installed")
required_apps = ['rest_framework', 'tracker']
missing = [app for app in required_apps if app not in settings.INSTALLED_APPS]
if not missing:
    print(f"  ✅ PASS - All apps installed")
else:
    print(f"  ❌ FAIL - Missing: {missing}")

# Test 3: Migrations Applied
print("\n✓ Test 3: Database Migrations")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM django_migrations;")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"  ✅ PASS - {count} migrations applied")
        else:
            print(f"  ❌ FAIL - No migrations found")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

# Test 4: Superuser Exists
print("\n✓ Test 4: Superuser Created")
try:
    if User.objects.filter(is_superuser=True).exists():
        print(f"  ✅ PASS - Superuser exists")
    else:
        print(f"  ⚠️  WARNING - No superuser found")
except Exception as e:
    print(f"  ❌ FAIL - {e}")

print("\n" + "="*50)
print("TICKET 1 COMPLETE!")
print("="*50 + "\n")