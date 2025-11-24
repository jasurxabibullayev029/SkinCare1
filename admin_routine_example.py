#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from accounts.models import CustomUser
from routines.models import Routine

# Admin panel orqali routine qo'shish uchun to'liq misol
print("=== Admin Panel orqali Routine qo'shish misoli ===")
print()

# User tanlash
user = CustomUser.objects.first()
print(f"User: {user.username}")

# Routine qo'shish uchun JSON format
routine_data = {
    "name": "Утренняя рутина для сухой кожи",
    "routine_type": "morning",
    "is_ai_generated": False,
    "products": [
        "Мягкий гель для умывания",
        "Тоник с гиалуроновой кислотой",
        "Сыворотка с витамином С",
        "Увлажняющий крем"
    ],
    "steps": [
        {
            "step_number": 1,
            "step_name": "Очищение",
            "product": "Мягкий гель для умывания",
            "instructions": "Нанести небольшое количество геля на влажное лицо, массировать круговыми движениями 1-2 минуты, затем тщательно смыть теплой водой.",
            "duration_minutes": 2
        },
        {
            "step_number": 2,
            "step_name": "Тонизирование",
            "product": "Тоник с гиалуроновой кислотой",
            "instructions": "Нанести тоник на ватный диск и протереть лицо. Дать впитаться 1-2 минуты.",
            "duration_minutes": 1
        },
        {
            "step_number": 3,
            "step_name": "Сыворотка",
            "product": "Сыворотка с витамином С",
            "instructions": "Нанести 2-3 капли сыворотки на лицо, избегая области вокруг глаз. Легкими похлопывающими движениями распределить по коже.",
            "duration_minutes": 1
        },
        {
            "step_number": 4,
            "step_name": "Увлажнение",
            "product": "Увлажняющий крем",
            "instructions": "Нанести крем на лицо и шею легкими массажными движениями. Дать полностью впитаться.",
            "duration_minutes": 2
        }
    ]
}

print("\n=== Admin panelga kiring va quyidagilarni kiriting: ===")
print(f"User: {user.username}")
print(f"Name: {routine_data['name']}")
print(f"Routine Type: {routine_data['routine_type']}")
print(f"AI Generated: {routine_data['is_ai_generated']}")
print(f"Products (JSON): {routine_data['products']}")
print(f"Steps (JSON): {routine_data['steps']}")

print("\n=== Steps JSON ni nusxalab admin panelga kiriting: ===")
import json
print(json.dumps(routine_data['steps'], indent=2, ensure_ascii=False))

# Database qo'shish test
try:
    routine = Routine.objects.create(
        user=user,
        name=routine_data['name'],
        routine_type=routine_data['routine_type'],
        is_ai_generated=routine_data['is_ai_generated'],
        products=routine_data['products'],
        steps=routine_data['steps']
    )
    print(f"\n✅ Routine muvaffaqiyatli yaratildi: {routine.name} (ID: {routine.id})")
    print(f"Steps count: {len(routine.steps)}")
except Exception as e:
    print(f"\n❌ Xatolik: {e}")
