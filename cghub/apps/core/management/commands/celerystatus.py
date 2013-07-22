import datetime
import time

from djcelery.models import TaskState

from django.core.management.base import BaseCommand
from django.utils import timezone

from cghub.apps.core.utils import is_celery_alive
from cghub.apps.core.tasks import dummy_task


class Command(BaseCommand):
    help = 'Checks celery status.'

    def handle(self, *args, **options):
        if not is_celery_alive():
            self.stdout.write('Celery is unavailable.\n')
            return
        self.stdout.write('Creating dummy task.\n')
        now = timezone.now()
        result = dummy_task.delay(now)
        next_day = result.get(timeout=60)
        if next_day == now + datetime.timedelta(days=1):
            # check celeryevcam
            # TaskState updates every 1s
            time.sleep(2)
            try:
                state = TaskState.objects.get(task_id=result.task_id)
            except TaskState.DoesNotExist:
                self.stdout.write('Result was not saved to TaskState table. '
                            'Please check that celeryevcam works.\n')
                return
            self.stdout.write('Celery works.\n')
            return
        self.stdout.write('Timeout, dummy task was not done.\n')
