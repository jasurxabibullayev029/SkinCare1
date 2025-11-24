#!/usr/bin/env python
"""
Test script to check user model and database status
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from django.contrib.auth import get_user_model

def test_user_model():
    print("🧪 Testing User Model Configuration...")

    User = get_user_model()
    print(f"✅ Using user model: {User.__name__}")
    print(f"✅ User model module: {User.__module__}")

    # Check if model has skin_type attribute
    has_skin_type = hasattr(User, 'skin_type')
    print(f"✅ User model has skin_type attribute: {has_skin_type}")

    if has_skin_type:
        # Check the field definition
        skin_type_field = User._meta.get_field('skin_type')
        print(f"✅ skin_type field: {skin_type_field}")
        print(f"✅ skin_type choices: {skin_type_field.choices}")

    # Check existing users
    try:
        users = User.objects.all()
        print(f"✅ Number of users in database: {users.count()}")

        # Show first few users
        for i, user in enumerate(users[:3]):
            print(f"✅ User {i+1}: {user.username}")
            if has_skin_type:
                print(f"   skin_type: {getattr(user, 'skin_type', 'Not set')}")
                print(f"   age: {getattr(user, 'age', 'Not set')}")
                print(f"   lifestyle: {getattr(user, 'lifestyle', 'Not set')[:50] if getattr(user, 'lifestyle', None) else 'Not set'}")

    except Exception as e:
        print(f"❌ Error accessing users: {e}")

    print("🎉 User model test completed!")

if __name__ == '__main__':
    test_user_model()
