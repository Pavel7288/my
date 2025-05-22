import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # ключ всегда такой и путь к попке settings

app = Celery('app')  # это просто имя твоего Celery-приложения можно любое поставить, но так понятнее
app.config_from_object('django.conf:settings', namespace='CELERY') #'CELERY' — это значит, что Celery будет искать
# все настройки, которые начинаются с префикса CELERY_ в файле settings. первое встроенный модуль Django берет данные из
app.autodiscover_tasks()  # говорит искать задачи (функции @shared_task) во всех установленных приложениях в installed_apps