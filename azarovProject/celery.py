import os
from celery import Celery
from celery.schedules import crontab

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'azarovProject.settings')

app = Celery('azarovProject')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

# # заносим таски в очередь
# app.conf.beat_schedule = {
#     'every': {
#         'task': '<name_of_app>.tasks.repeat_order_make',
#         'schedule': crontab(),# по умолчанию выполняет каждую минуту, очень гибко
#     },                                                              # настраивается
# }