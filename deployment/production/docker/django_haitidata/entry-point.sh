#!/usr/bin/env bash

# Run database migrations
echo "Run database migrations"
python manage.py makemigrations --noinput --merge

# Run collectstatic
echo "Run collectstatic"
python manage.py collectstatic --noinput


uwsgi --ini /uwsgi.conf
