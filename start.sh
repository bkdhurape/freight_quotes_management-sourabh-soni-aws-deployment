#!/bin/bash
cd cms

cp .env.beta .env

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
# gunicorn --workers 1 -b 0.0.0.0:${APP_PORT} --access-logfile logs/gunicorn-access.log --error-logfile logs/gunicorn-errors.log subscription_app.wsgi

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
# python manage.py runserver 0.0.0.0:8000
