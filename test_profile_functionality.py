#!/usr/bin/env python
"""
Test script to verify profile editing functionality is working correctly
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

def test_profile_functionality():
    print("🧪 Testing Profile Editing Functionality...")

    # Create test client
    client = Client()

    # Test 1: Check if profile URL exists and requires authentication
    print("\n1️⃣ Testing profile URL accessibility...")
    try:
        response = client.get('/profile/')
        if response.status_code == 302:  # Redirect to login
            print("✅ Profile page requires authentication (redirects to login)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing profile URL: {e}")

    # Test 2: Create a test user
    print("\n2️⃣ Creating test user...")
    try:
        # Clean up any existing test user
        User.objects.filter(username='testuser_profile').delete()

        # Create test user
        test_user = User.objects.create_user(
            username='testuser_profile',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        # Update custom fields
        test_user.skin_type = 'dry'
        test_user.age = 25
        test_user.lifestyle = 'Active lifestyle'
        test_user.skin_concerns = 'Dry skin issues'
        test_user.save()

        print("✅ Test user created successfully")

        # Test 3: Login as test user
        print("\n3️⃣ Testing user login...")
        login_response = client.post('/login/', {
            'username': 'testuser_profile',
            'password': 'testpass123'
        })

        if login_response.status_code == 302 and 'profile' in login_response.get('Location', ''):
            print("✅ User login successful")

            # Test 4: Access profile page
            print("\n4️⃣ Testing profile page access...")
            profile_response = client.get('/profile/')
            if profile_response.status_code == 200:
                print("✅ Profile page accessible")

                # Check if user data is in response
                if 'Test User' in profile_response.content.decode():
                    print("✅ User data displayed correctly")
                else:
                    print("❌ User data not displayed properly")

                # Test 5: Test profile editing
                print("\n5️⃣ Testing profile editing...")
                edit_response = client.post('/profile/', {
                    'first_name': 'Updated',
                    'last_name': 'Name',
                    'email': 'updated@example.com',
                    'skin_type': 'oily',
                    'age': '30',
                    'lifestyle': 'Updated lifestyle',
                    'skin_concerns': 'Updated skin concerns'
                })

                if edit_response.status_code == 302:  # Redirect after successful edit
                    print("✅ Profile edit form submitted successfully")

                    # Check if user data was updated
                    test_user.refresh_from_db()
                    if test_user.first_name == 'Updated' and test_user.email == 'updated@example.com':
                        print("✅ User data updated in database")
                    else:
                        print("❌ User data not updated in database")
                else:
                    print(f"❌ Profile edit failed with status: {edit_response.status_code}")

            else:
                print(f"❌ Profile page not accessible: {profile_response.status_code}")
        else:
            print("❌ User login failed")

        # Cleanup
        test_user.delete()
        print("✅ Test user cleaned up")

    except Exception as e:
        print(f"❌ Error during testing: {e}")

    print("\n🎉 Profile functionality test completed!")

if __name__ == '__main__':
    test_profile_functionality()
