import os
from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Celery('avsoft',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['celery_module.tasks'])
app.autodiscover_tasks()
