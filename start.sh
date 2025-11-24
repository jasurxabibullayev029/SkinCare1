#!/bin/bash

# Exit on error
set -o errexit

# Set the Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Debug info
echo "=== Starting SkinCare AI ==="
echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Files in current directory:"
ls -la

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if not exists
echo "Checking for superuser..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')).exists():
        User.objects.create_superuser(
            os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'),
            os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
            os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')
        )
        print('Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {e}'
)"

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn skincare_ai.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 3 \
    --pythonpath $PWD \
    --log-file - \
    --timeout 120 \
    --worker-class gthread \
    --threads 2
