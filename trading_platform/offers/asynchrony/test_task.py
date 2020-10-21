import os
import django
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_platform.settings')
django.setup()
app = Celery('trading_platform')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from time import sleep

from datetime import datetime

@app.task
def hello_world():
    t = datetime.now()
    sleep(3)  # поставим тут задержку в 10 сек для демонстрации ассинхрности
    return str(t)
