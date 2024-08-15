#!/bin/bash
echo "Create static..."
python /app/manage.py collectstatic
cp -r /app/collected_static/. /static/django_static/
echo "...static created."