#!/bin/bash

# Starting Redis
echo "Starting Redis..."
redis-server &

# Starting Celery Worker
echo "Starting Celery Worker..."
celery -A celery_app.app worker --loglevel=info &

# Starting Flower for Celery monitoring
echo "Starting Flower..."
celery -A celery_app.app flower &

# Starting Django Development Server
echo "Starting Django Development Server..."
python manage.py runserver