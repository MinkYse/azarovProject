# your_app/tasks.py
from celery import shared_task
from .models import Child


@shared_task
def reset_is_paid():
    Child.objects.filter(is_vip=False).update(is_paid=False)
