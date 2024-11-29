from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly_newsletter': {
        'task': 'send_weekly_newsletter',
        'schedule': crontab(minute=0, hour=8, day_of_week=0),  # Каждый понедельник в 8:00
    },
}
