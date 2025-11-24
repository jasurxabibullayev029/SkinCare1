#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from django.urls import reverse

print('=== Routines URL Debug ===')
try:
    api_url = reverse('routine_list_create')
    print(f'API URL: {api_url}')
except Exception as e:
    print(f'Error: {e}')

# Check if routine creation works
from routines.models import Routine, RoutineStep
print(f'Routine count: {Routine.objects.count()}')
print(f'RoutineStep count: {RoutineStep.objects.count()}')
