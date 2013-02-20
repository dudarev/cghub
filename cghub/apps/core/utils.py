import urllib
import traceback

from django.core.mail import mail_admins


ALLOWED_ATTRIBUTES = [
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
    ]

def get_filters_string(attributes):
    filter_str = ''
    for attr in ALLOWED_ATTRIBUTES:
        if attributes.get(attr):
                filter_str += '&%s=%s' % (
                    attr,
                    urllib.quote(attributes.get(attr))
                )
    return filter_str

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
