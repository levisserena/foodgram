#!/bin/bash

echo "Makemigrations and migrate..."
python manage.py makemigrations
python manage.py migrate
echo "...migrations are over."