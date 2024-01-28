#!/bin/bash

cleanup() {
    echo "Stopping Django Development Server..."
    kill %5  # Stop Django

    echo "Stopping Flower..."
    kill %4  # Stop Flower

    echo "Stopping Celery Beat..."
    kill %3  # Stop Celery Beat

    echo "Stopping Celery Worker..."
    kill %2  # Stop Celery Worker

    echo "Stopping Redis..."
    kill %1  # Stop Redis

    exit 0  # Exit the script
}

# Set a trap for the SIGINT signal (Ctrl+C)
trap 'cleanup' SIGINT

echo "Starting Redis..."
redis-server &

echo "Starting Celery Worker..."
celery -A smartschedule.celery.app worker --loglevel=info &

echo "Starting Celery Beat..."
celery -A smartschedule.celery.app beat --loglevel=info &

echo "Starting Flower..."
celery -A smartschedule.celery.app flower &

echo "Starting Django Development Server..."
python manage.py runserver

wait
