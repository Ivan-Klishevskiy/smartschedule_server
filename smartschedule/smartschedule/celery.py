import os,django
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartschedule.settings')
django.setup()
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from event_manager.tasks import collect_script_contents_gout_task




app = Celery('smartschedule')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'collect-script-contents-every-5-minutes': {
        'task': 'event_manager.tasks.collect_script_contents_gout_task',
        'schedule': crontab(minute='*/5'),
    },
}
