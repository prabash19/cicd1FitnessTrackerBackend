import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_tracker.settings')
django.setup()

from django.db import connection

def test_database_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print("✅ Database connection successful!")
            print(f"PostgreSQL version: {db_version[0]}")
            
            # Test user table
            cursor.execute("SELECT COUNT(*) FROM auth_user;")
            user_count = cursor.fetchone()
            print(f"✅ Users in database: {user_count[0]}")
            
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()