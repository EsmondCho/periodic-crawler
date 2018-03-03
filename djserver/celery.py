from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djserver.settings')

app = Celery('djserver')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    BROKER_URL='pyamqp://guest@localhost//',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_RESULT_BACKEND="django-db",
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE={
        'crawling_clien': {
            'task': 'crawler.tasks.crawling_clien',
            'schedule': crontab(minute='*/30'),
            'args': (str(datetime.now()), 1, False)
        }
    }
)
