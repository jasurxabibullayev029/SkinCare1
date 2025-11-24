#!/bin/bash

# Exit on error
set -o errexit

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start Gunicorn
exec gunicorn skincare_ai.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 3 \
    --pythonpath $PWD \
    --log-file -
