#!/bin/bash

echo "Сбор статики..."
python manage.py collectstatic --noinput
echo "Собрали статику"

echo "Ждем postgres ..."
./wait-for-it.sh db:5432
echo "Postgres на базе"

echo "Делаем миграции ..."
./manage.py migrate
echo "Миграции сделаны"

echo "Делаем фикстуры ..."
./manage.py loaddata fixtures/good/categories.json
./manage.py loaddata fixtures/good/products.json
echo "Фикстуры сделаны"

echo "Делаем бога ..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='bublik').exists():
    User.objects.create_superuser(username='bublik', email='k7288@gmai.com', password='p',number='+1243434345')
EOF
echo "Бог сделан"

echo "Запуск Gunicorn..."
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000
echo "Всё летает"