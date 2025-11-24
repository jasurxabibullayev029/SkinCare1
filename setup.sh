#!/bin/bash

# Exit on error
set -o errexit

echo "🧴 SkinCare AI - Render Deployment Setup"
echo "===================================="

# Set Python version
PYTHON_VERSION=${PYTHON_VERSION:-3.9.0}

echo "🐍 Using Python version: $PYTHON_VERSION"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x start.sh

# Create necessary directories
echo "📂 Creating necessary directories..."
mkdir -p staticfiles
mkdir -p media

# Set proper permissions
echo "🔒 Setting permissions..."
chmod -R 755 .

# Verify Django settings
echo "🔍 Verifying Django settings..."
python manage.py check --deploy

echo "✅ Setup completed successfully!"
echo "🚀 Start the application with: ./start.sh"
echo "⚙️ Setting up Django..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating admin user..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@skincare.ai', 'admin123')" | python manage.py shell

# Populate sample data
echo "🌱 Populating sample data..."
python manage.py populate_sample_data

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To run the application:"
echo "1. Backend: python manage.py runserver"
echo "2. Frontend: cd frontend && npm install && npm start"
echo ""
echo "Default admin credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Don't forget to:"
echo "1. Set your OpenAI API key in .env file"
echo "2. Configure email settings if needed"
echo "3. Update database settings for production"
