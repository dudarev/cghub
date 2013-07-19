import datetime

from celery.task import task


@task()
def dummy_task(date):
    """
    Dummy task, used for checking is celery works properly.
    Returns date + 1 day.
    """
    return date + datetime.timedelta(days=1)
