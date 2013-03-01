import urllib
import traceback
import hashlib

from django.core.mail import mail_admins
from django.conf import settings


ALLOWED_ATTRIBUTES = (
        'study',
        'center_name',
        'last_modified',
        'upload_date',
        'analyte_code',
        'sample_type',
        'library_strategy',
        'disease_abbr',
        'state',
        'refassem_short_name',
    )

WSAPI_SETTINGS_LIST = (
        'CGHUB_SERVER',
        'CGHUB_ANALYSIS_ID_URI',
        'CGHUB_ANALYSIS_ATTRIBUTES_URI',
        'USE_CACHE',
        'CACHE_BACKEND',
        'CACHE_DIR',
    )


def get_filters_string(attributes):
    filter_str = ''
    for attr in ALLOWED_ATTRIBUTES:
        if attributes.get(attr):
                filter_str += '&%s=%s' % (
                    attr,
                    urllib.quote(attributes.get(attr))
                )
    return filter_str


def get_wsapi_settings():
    wsapi_settings = {}
    for name in WSAPI_SETTINGS_LIST:
        setting = getattr(settings, 'WSAPI_%s' % name, None)
        if setting != None:
            wsapi_settings[name] = setting
    return wsapi_settings


def generate_task_uuid(**d):
    """
    Generate uuid from dict
    """
    result = [str(v) for v in d.values()]
    result.sort()
    md5 = hashlib.md5(''.join(result))
    return md5.hexdigest()


def is_celery_alive():
    """
    Return 'True' if celery works properly
    """
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            return False
        return True
    except Exception:
        subject = '[ucsc-cghub] ERROR: Message broker not working'
        message = traceback.format_exc()
        mail_admins(subject, message, fail_silently=True)
        return False
