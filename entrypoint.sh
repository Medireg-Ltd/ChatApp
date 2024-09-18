#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

mkdir -p static
mkdir -p media
# Apply database migrations
python manage.py makemigrations
python manage.py makemigrations accounts chat
python manage.py migrate

# Collect static files (optional, if your app serves static files)
# python manage.py collectstatic --noinput

# Start Gunicorn server
exec "$@"
