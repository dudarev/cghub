import glob
import datetime
import os

from django.conf import settings
from celery.task import task
from cghub.wsapi.api import request as api_request
from cghub.apps.core.utils import get_wsapi_settings


WSAPI_SETTINGS = get_wsapi_settings()


@task(ignore_result=True)
def cache_results_task(file_dict):
    analysis_id = file_dict.get('analysis_id')
    filename_with_attributes = os.path.join(settings.CART_CACHE_FOLDER,
        "{0}_with_attributes".format(analysis_id))
    filename_without_attributes = os.path.join(settings.CART_CACHE_FOLDER,
        "{0}_without_attributes".format(analysis_id))
    if os.path.isfile(filename_with_attributes) and os.path.isfile(filename_without_attributes):
        return
    result = api_request(
                query='analysis_id={0}'.format(analysis_id),
                settings=WSAPI_SETTINGS)
    with open(filename_with_attributes, 'w') as f:
        f.write(result.tostring())
    with open(filename_without_attributes, 'w') as f:
        result.remove_attributes()
        f.write(result.tostring())


@task(ignore_result=True)
def cache_clear_task():
    files = glob.glob(os.path.join(settings.CART_CACHE_FOLDER, '*'))
    now = datetime.datetime.now()
    for file in files:
        time_file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        if now - time_file_modified > settings.TIME_DELETE_CART_CACHE_FILES_OLDER:
            os.remove(file)
