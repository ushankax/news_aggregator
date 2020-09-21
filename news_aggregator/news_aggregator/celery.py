from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from . import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings')

app = Celery('news_aggregator')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = settings.BROKER_URL
app.conf.broker_transport_options = settings.BROKER_TRANSPORT_OPTIONS
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
