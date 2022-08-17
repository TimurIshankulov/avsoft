import os
from celery import Celery
from config import (CELERY_BROKER_URL, CELERY_BROKER_TRANSPORT_OPTIONS, CELERY_ACCEPT_CONTENT,
                    CELERY_RESULT_BACKEND, CELERY_RESULT_SERIALIZER, CELERY_TASK_SERIALIZER)

app = Celery('avsoft',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['celery_module.tasks'])
app.autodiscover_tasks()
