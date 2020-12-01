import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_platform.settings')
app = Celery('trading_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_offers_script': {
        'task': 'offers.tasks.check_offers',
        'schedule': 10.0,
    },
}
