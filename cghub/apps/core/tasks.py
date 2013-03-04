from django.conf import settings
from django.utils import timezone
from celery.task import task

from cghub.wsapi.utils import clear_cache


@task(ignore_result=True)
def api_cache_clear_task():
    """
    Task to clear API cache.
    """
    now = timezone.now()
    clear_cache(
            cache_dir=settings.WSAPI_CACHE_DIR,
            older_than=now - settings.TIME_DELETE_API_CACHE_FILES_OLDER)
