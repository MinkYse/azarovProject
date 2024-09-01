from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask

import payments.tasks


class Command(BaseCommand):
    help = 'Creates periodic task for fetching new emails from Yandex'

    def handle(self, *args, **kwargs):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute='*',
            hour='*',
            day_of_month='*',
            month_of_year='*',
            day_of_week='*'
        )

        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='Reset is_paid field for non-VIP children',
            task='payments.tasks.reset_is_paid',
        )
        self.stdout.write(self.style.SUCCESS('Successfully created periodic task'))
