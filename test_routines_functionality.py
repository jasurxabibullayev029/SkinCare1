#!/usr/bin/env python
"""
Test script to verify routines functionality is working correctly
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from routines.models import Routine

def test_routines_functionality():
    print("🧪 Testing Routines Functionality...")

    # Create test client
    client = Client()

    # Test 1: Check if routines URL is accessible
    print("\n1️⃣ Testing routines URL accessibility...")
    try:
        # Test unauthenticated access (should redirect)
        response = client.get('/routines/')
        if response.status_code == 302:  # Redirect to login
            print("✅ Routines requires authentication (redirects to login)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing routines URL: {e}")

    # Test 2: Create and login test user
    print("\n2️⃣ Creating and logging in test user...")
    try:
        # Clean up any existing test user
        User.objects.filter(username='test_routines_user').delete()

        # Create test user
        test_user = User.objects.create_user(
            username='test_routines_user',
            email='routines@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Routines',
            skin_type='dry'  # Set skin type for AI generation
        )
        test_user.save()

        # Login
        login_response = client.post('/login/', {
            'username': 'test_routines_user',
            'password': 'testpass123'
        })

        if login_response.status_code == 302 and 'profile' in login_response.get('Location', ''):
            print("✅ User login successful")
        else:
            print("❌ User login failed")
            return

        # Test 3: Access routines page
        print("\n3️⃣ Testing routines page access...")
        routines_response = client.get('/routines/')
        if routines_response.status_code == 200:
            print("✅ Routines page accessible")

            # Check if modal forms are present
            content = routines_response.content.decode()
            if 'generateModal' in content:
                print("✅ Generate modal form present")
            else:
                print("❌ Generate modal form missing")

            if 'customModal' in content:
                print("✅ Custom modal form present")
            else:
                print("❌ Custom modal form missing")

            # Check if routines grid is present
            if 'routinesGrid' in content:
                print("✅ Routines grid present")
            else:
                print("❌ Routines grid missing")

        else:
            print(f"❌ Routines page not accessible: {routines_response.status_code}")

        # Test 4: Test AI routine generation
        print("\n4️⃣ Testing AI routine generation...")
        generate_response = client.post('/routines/', {
            'action': 'generate_routine',
            'routine_type': 'morning'
        })

        if generate_response.status_code == 302:  # Redirect after successful generation
            print("✅ AI routine generation form submitted successfully")

            # Check if routine was created in database
            routine_count = Routine.objects.filter(user=test_user).count()
            if routine_count > 0:
                print(f"✅ AI routine created in database ({routine_count} routines)")

                # Check routine details
                latest_routine = Routine.objects.filter(user=test_user).latest('created_at')
                if latest_routine.is_ai_generated:
                    print("✅ Routine marked as AI generated")
                else:
                    print("❌ Routine not marked as AI generated")

                if len(latest_routine.steps) > 0:
                    print(f"✅ Routine has {len(latest_routine.steps)} steps")
                else:
                    print("❌ Routine has no steps")
            else:
                print("❌ AI routine not created in database")
        else:
            print(f"❌ AI routine generation failed with status: {generate_response.status_code}")

        # Test 5: Test custom routine creation
        print("\n5️⃣ Testing custom routine creation...")
        import json

        # Create steps data
        steps_data = [
            {
                'step_number': 1,
                'step_name': 'Очищение',
                'product': 'Очищающая пенка',
                'instructions': 'Нанесите пенку на влажное лицо',
                'duration_minutes': 2
            },
            {
                'step_number': 2,
                'step_name': 'Тонизирование',
                'product': 'Тоник',
                'instructions': 'Протрите лицо тоником',
                'duration_minutes': 1
            }
        ]

        custom_response = client.post('/routines/', {
            'action': 'create_custom_routine',
            'name': 'Моя тестовая рутина',
            'routine_type': 'evening',
            'steps': json.dumps(steps_data)
        })

        if custom_response.status_code == 302:  # Redirect after successful creation
            print("✅ Custom routine creation form submitted successfully")

            # Check if custom routine was created
            custom_routine_count = Routine.objects.filter(user=test_user, is_ai_generated=False).count()
            if custom_routine_count > 0:
                print(f"✅ Custom routine created in database ({custom_routine_count} custom routines)")

                # Check if steps were saved correctly
                custom_routine = Routine.objects.filter(user=test_user, is_ai_generated=False).latest('created_at')
                if len(custom_routine.steps) == 2:
                    print("✅ Custom routine steps saved correctly")
                else:
                    print(f"❌ Custom routine steps count incorrect: {len(custom_routine.steps)}")
            else:
                print("❌ Custom routine not created in database")
        else:
            print(f"❌ Custom routine creation failed with status: {custom_response.status_code}")

        # Test 6: Check if routines are displayed
        print("\n6️⃣ Testing routines display...")
        display_response = client.get('/routines/')
        if display_response.status_code == 200:
            content = display_response.content.decode()

            # Check if routines are displayed
            if 'Моя тестовая рутина' in content or 'AI рутина' in content:
                print("✅ Routines displayed correctly in template")
            else:
                print("❌ Routines not displayed in template")

        # Cleanup
        test_user.delete()
        print("✅ Test user cleaned up")

    except Exception as e:
        print(f"❌ Error during testing: {e}")

    print("\n🎉 Routines functionality test completed!")

if __name__ == '__main__':
    test_routines_functionality()
