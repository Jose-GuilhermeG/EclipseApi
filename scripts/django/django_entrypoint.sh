#!/bin/bash
echo "Waiting for MySQL to be ready..."

while ! nc -z db 3306; do
  sleep 1
done

echo "MySQL is up - running migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py loaddata users.json
echo "Starting Django Server..."
exec "$@"
