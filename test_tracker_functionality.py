#!/usr/bin/env python
"""
Test script to verify tracker functionality is working correctly
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from tracker.models import ProgressEntry, SkinMetric

def test_tracker_functionality():
    print("🧪 Testing Tracker Functionality...")

    # Create test client
    client = Client()

    # Test 1: Check if tracker URL is accessible
    print("\n1️⃣ Testing tracker URL accessibility...")
    try:
        # Test unauthenticated access (should redirect)
        response = client.get('/tracker/')
        if response.status_code == 302:  # Redirect to login
            print("✅ Tracker requires authentication (redirects to login)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing tracker URL: {e}")

    # Test 2: Create and login test user
    print("\n2️⃣ Creating and logging in test user...")
    try:
        # Clean up any existing test user
        User.objects.filter(username='test_tracker_user').delete()

        # Create test user
        test_user = User.objects.create_user(
            username='test_tracker_user',
            email='tracker@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Tracker'
        )
        test_user.save()

        # Login
        login_response = client.post('/login/', {
            'username': 'test_tracker_user',
            'password': 'testpass123'
        })

        if login_response.status_code == 302 and 'profile' in login_response.get('Location', ''):
            print("✅ User login successful")
        else:
            print("❌ User login failed")
            return

        # Test 3: Access tracker page
        print("\n3️⃣ Testing tracker page access...")
        tracker_response = client.get('/tracker/')
        if tracker_response.status_code == 200:
            print("✅ Tracker page accessible")

            # Check if modal form is present
            if 'addEntryModal' in tracker_response.content.decode():
                print("✅ Modal form present in template")
            else:
                print("❌ Modal form missing from template")

            # Check if entries container is present
            if 'entriesContainer' in tracker_response.content.decode():
                print("✅ Entries container present")
            else:
                print("❌ Entries container missing")

        else:
            print(f"❌ Tracker page not accessible: {tracker_response.status_code}")

        # Test 4: Test adding a progress entry
        print("\n4️⃣ Testing add entry functionality...")
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')

        add_response = client.post('/tracker/', {
            'date': today,
            'skin_condition': 'improved',
            'notes': 'Test entry for tracker functionality',
            'hydration': '8',
            'oiliness': '3',
            'redness': '2',
            'acne': '4',
            'wrinkles': '5',
            'pores': '6'
        })

        if add_response.status_code == 302:  # Redirect after successful submission
            print("✅ Progress entry form submitted successfully")

            # Check if entry was created in database
            entry_count = ProgressEntry.objects.filter(user=test_user).count()
            if entry_count > 0:
                print(f"✅ Progress entry created in database ({entry_count} entries)")

                # Check if metrics were created
                latest_entry = ProgressEntry.objects.filter(user=test_user).latest('created_at')
                metrics_count = SkinMetric.objects.filter(entry=latest_entry).count()
                if metrics_count > 0:
                    print(f"✅ Skin metrics created ({metrics_count} metrics)")
                else:
                    print("❌ Skin metrics not created")
            else:
                print("❌ Progress entry not created in database")
        else:
            print(f"❌ Add entry failed with status: {add_response.status_code}")

        # Test 5: Check if entries are displayed
        print("\n5️⃣ Testing entries display...")
        display_response = client.get('/tracker/')
        if display_response.status_code == 200:
            content = display_response.content.decode()

            # Check if entries are displayed
            if 'Test entry for tracker functionality' in content:
                print("✅ Entries displayed correctly in template")
            else:
                print("❌ Entries not displayed in template")

        # Cleanup
        test_user.delete()
        print("✅ Test user cleaned up")

    except Exception as e:
        print(f"❌ Error during testing: {e}")

    print("\n🎉 Tracker functionality test completed!")

if __name__ == '__main__':
    test_tracker_functionality()
