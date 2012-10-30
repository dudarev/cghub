import datetime
import settings
from celery.task import task
from utils import clear_cache


@task(ignore_result=True)
def api_cache_clear_task():
    """
    Task to clear API cache which is by default is stored in
    `/tmp/wsapi/`.
    """
    now = datetime.datetime.now()
    clear_cache(now - settings.TIME_DELETE_API_CACHE_FILES_OLDER)
