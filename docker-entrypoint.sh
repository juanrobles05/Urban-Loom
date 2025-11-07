#!/bin/bash
set -e

echo "🚀 Starting Urban-Loom application..."

# Wait for database to be ready (if using PostgreSQL)
if [ "$DATABASE_ENGINE" = "django.db.backends.postgresql" ]; then
    echo "⏳ Waiting for PostgreSQL..."
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done
    echo "✅ PostgreSQL is ready!"
fi

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser if needed..."
python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(email='admin@urbanloom.com').exists():
    User.objects.create_superuser(
        email='admin@urbanloom.com',
        first_name='Admin',
        last_name='Urban Loom',
        phone_number='0000000000',
        password='admin123'
    )
    print('✅ Superuser created: admin@urbanloom.com / admin123')
else:
    print('ℹ️ Superuser already exists')
"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create media directories
echo "📁 Creating media directories..."
mkdir -p mediafiles/categories mediafiles/collections mediafiles/products mediafiles/profile_pictures

echo "✅ Setup complete! Starting application..."

# Execute the main command
exec "$@"
