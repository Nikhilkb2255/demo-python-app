#!/bin/bash

# Django Demo App Runner
# Simple script to run the Django demo application

echo "🚀 Starting Django Demo App..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py not found. Please run this script from the Django project root directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/pyvenv.cfg" ] || [ requirements.txt -nt venv/pyvenv.cfg ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Create superuser if not exists
echo "👤 Setting up admin user..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Admin user created: admin/admin123')
else:
    print('✅ Admin user already exists')
"

# Create sample data if database is empty
echo "📊 Creating sample data..."
python manage.py create_sample_data --count 10

echo ""
echo "🎉 Django Demo App is ready!"
echo ""
echo "🌐 Access Points:"
echo "   Main App:     http://localhost:8000"
echo "   Admin Panel:  http://localhost:8000/admin/"
echo "   API Test:     http://localhost:8000/api/test/"
echo "   API Health:   http://localhost:8000/api/health/"
echo "   API Products: http://localhost:8000/api/products/"
echo ""
echo "👤 Admin Login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
python manage.py runserver
