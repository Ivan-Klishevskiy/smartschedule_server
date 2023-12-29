#!/bin/bash

echo "Create migrations"
python manage.py makemigrations smartschedule
echo "======================================"

echo "Migrate"
python manage.py migrate
echo "======================================"

echo "Loading fixtures"
python manage.py loaddata event_initial_data.json
echo "======================================"

echo "Creating superuser"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python manage.py shell
echo "======================================"

echo "Start server"
python manage.py runserver 0.0.0.0:8000