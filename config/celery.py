import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('library_kg')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clean-expired-sessions-every-night': {
        'task': 'common.tasks.clear_expired_sessions_task',
        'schedule': crontab(hour=3, minute=0),
    },
}
