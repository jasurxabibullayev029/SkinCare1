#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.models import CustomUser
from routines.views import RoutineListCreateView

# Test the actual API endpoint
print('=== Testing API Endpoint ===')

user = CustomUser.objects.first()
print(f'Test user: {user.username}')

# Test data that matches JavaScript exactly
test_data = {
    'name': 'Test Routine API',
    'routine_type': 'morning',
    'products': [],
    'steps': [
        {
            'step_number': 1,
            'step_name': 'Очищение',
            'product': 'Пенка для умывания',
            'instructions': 'Следуйте инструкциям на продукте',
            'duration_minutes': 5
        }
    ]
}

# Create request
factory = RequestFactory()
request = factory.post('/api/', data=json.dumps(test_data), content_type='application/json')

# Add user to request
request.user = user

# Test the view directly
view = RoutineListCreateView()
view.request = request
view.format_kwarg = None

try:
    response = view.post(request)
    print(f'Status Code: {response.status_code}')
    print(f'Response Data: {response.data}')
    print('SUCCESS: API endpoint works!')
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
