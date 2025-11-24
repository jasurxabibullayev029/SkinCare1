#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from accounts.models import CustomUser
from routines.models import Routine

# Test routine detail page functionality
print("=== Testing Routine Detail Page ===")

user = CustomUser.objects.first()
routines = Routine.objects.filter(user=user)

if routines:
    routine = routines.first()
    print(f"Routine: {routine.name}")
    print(f"Steps count: {len(routine.steps)}")
    print(f"Steps data:")
    for i, step in enumerate(routine.steps):
        print(f"  {i+1}. {step.get('step_name', 'N/A')} - {step.get('duration_minutes', 0)} min")
    
    print(f"\nURL: http://127.0.0.1:8000/routines/web/{routine.id}/")
    print("\n✅ '← Предыдущий' va 'Следующий →' tugmalari ishlashi kerak!")
else:
    print("❌ Routine topilmadi. Avval routine yarating!")
