import os
import time

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartschedule.settings')

app = Celery('smartschedule')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'collect-script-contents-every-3-minutes': {
#         'task': '.tasks.collection_task',
#         'schedule': crontab(minute='*/3')
#     },
# }