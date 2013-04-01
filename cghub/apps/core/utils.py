import sys
import urllib
import traceback
import hashlib

from django.core.mail import mail_admins
from django.conf import settings

from cghub.apps.core.filters_storage import ALL_FILTERS


ALLOWED_ATTRIBUTES = ALL_FILTERS.keys()

DATE_ATTRIBUTES = (
        'last_modified',
        'upload_date',
    )

WSAPI_SETTINGS_LIST = (
        'CGHUB_SERVER',
        'CGHUB_ANALYSIS_ID_URI',
        'CGHUB_ANALYSIS_FULL_URI',
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


def get_default_query():
    """
    Taking in mind settings.DEFAULT_FILTERS returns query string.
    For example:
    DEFAULT_FILTERS = {
        'study': ('phs000178', '*Other_Sequencing_Multiisolate'),
        'state': ('live',),
        'upload_date': '[NOW-7DAY TO NOW]',
    }
    result should be:
    upload_date=[NOW-7DAY+TO+NOW]&study=(phs000178+OR+*Other_Sequencing_Multiisolate)&state=(live)
    """
    filters_list = []
    DEFAULT_FILTERS = settings.DEFAULT_FILTERS
    for f in DEFAULT_FILTERS:
        if f in ALLOWED_ATTRIBUTES:
            if f in DATE_ATTRIBUTES:
                filters_list.append('%s=%s' % (f, DEFAULT_FILTERS[f]))
            else:
                allowed_keys = ALL_FILTERS[f]['filters'].keys()
                filters_list.append('%s=(%s)' % (
                        f,
                        ' OR '.join([v for v in DEFAULT_FILTERS[f] if v in allowed_keys])
                ))
    return '&'.join(filters_list).replace(' ', '+')


def get_wsapi_settings():
    wsapi_settings = {}
    for name in WSAPI_SETTINGS_LIST:
        setting = getattr(settings, 'WSAPI_%s' % name, None)
        if setting != None:
            wsapi_settings[name] = setting
    return wsapi_settings


def generate_task_analysis_id(**d):
    """
    Generate analysis_id from dict
    """
    result = [str(v) for v in d.values()]
    result.sort()
    md5 = hashlib.md5(''.join(result))
    return md5.hexdigest()


def is_celery_alive():
    """
    Return 'True' if celery works properly
    """
    if 'test' in sys.argv:
        return True
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
