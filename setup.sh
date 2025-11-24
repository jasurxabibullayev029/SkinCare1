#!/bin/bash

echo "🧴 SkinCare AI Setup Script"
echo "=========================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
echo "🔼 Upgrading pip, setuptools and wheel to avoid build issues (Pillow/build deps)..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

# Setup Django
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
