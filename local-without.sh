#!/bin/bash

echo "Делаем миграции..."
./manage.py makemigrations
./manage.py migrate
echo "Миграции сделаны"

echo "Делаем celery воркера..."
celery -A app worker --loglevel=info &
echo "Сделан воркер"

echo "Запуск локально..."
exec ./manage.py runserver