#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from django.test import RequestFactory
from accounts.models import CustomUser
from routines.views import RoutineListCreateView
from routines.serializers import RoutineSerializer

# Test routine creation
print('=== Testing Routine Creation ===')

# Create test user
user = CustomUser.objects.first()
if not user:
    print('No users found!')
    exit()

print(f'Test user: {user.username}')

# Test data
test_data = {
    'name': 'Test Routine',
    'routine_type': 'morning',
    'products': [],
    'steps': [
        {
            'step_number': 1,
            'step_name': 'Очищение',
            'product': 'Пенка для умывания',
            'instructions': 'Нанести на влажное лицо',
            'duration_minutes': 2
        }
    ]
}

print('Test data:', json.dumps(test_data, indent=2, ensure_ascii=False))

# Test serializer
factory = RequestFactory()
request = factory.post('/api/', data=test_data, content_type='application/json')
request.user = user

serializer = RoutineSerializer(data=test_data, context={'request': request})
if serializer.is_valid():
    print('Serializer is valid!')
    routine = serializer.save()
    print(f'Created routine: {routine.name} (ID: {routine.id})')
    print(f'Steps: {routine.steps}')
else:
    print('Serializer errors:', serializer.errors)
