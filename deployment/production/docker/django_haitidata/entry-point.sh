#!/usr/bin/env bash

# Run database migrations
echo "Run database migrations"
python manage.py makemigrations --noinput --merge

# Run collectstatic
echo "Run collectstatic"
python manage.py collectstatic --noinput

if [ "$DEBUG" == "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
	uwsgi --ini /uwsgi.conf
fi