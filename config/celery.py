import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


app = Celery('test_task')
app.config_from_object(settings.CELERY)
app.autodiscover_tasks()
