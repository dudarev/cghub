import sys
import urllib
import traceback
import hashlib

from celery import states
from djcelery.models import TaskState

from django.core.mail import mail_admins
from django.conf import settings

from cghub.apps.core.filters_storage import ALL_FILTERS
from cghub.apps.core.attributes import DATE_ATTRIBUTES


ALLOWED_ATTRIBUTES = ALL_FILTERS.keys()


WSAPI_SETTINGS_LIST = (
        'CGHUB_SERVER',
        'CGHUB_ANALYSIS_ID_URI',
        'CGHUB_ANALYSIS_DETAIL_URI',
        'CGHUB_ANALYSIS_FULL_URI',
        'USE_CACHE',
        'CACHE_BACKEND',
        'CACHE_DIR',
        'HTTP_ERROR_ATTEMPTS',
        'HTTP_ERROR_SLEEP_AFTER',
    )


def get_filters_string(attributes):
    filter_str = ''
    for attr in ALLOWED_ATTRIBUTES:
        if attributes.get(attr):
                filter_str += '&%s=%s' % (
                    attr,
                    attributes.get(attr)
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
    return '&'.join(filters_list).replace('+', ' ')


def paginator_params(request):
    """
    Returns offset, limit.
    :param request: django Request object
    """
    offset = request.GET.get('offset')
    offset = offset and offset.isdigit() and int(offset) or 0
    limit = request.GET.get('limit')
    if limit and limit.isdigit():
        limit = int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
    elif request.COOKIES.has_key(settings.PAGINATOR_LIMIT_COOKIE):
        limit = request.COOKIES[settings.PAGINATOR_LIMIT_COOKIE]
        limit = limit.isdigit() and int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
    else:
        limit = settings.DEFAULT_PAGINATOR_LIMIT
    return offset, limit


def get_wsapi_settings():
    wsapi_settings = {}
    for name in WSAPI_SETTINGS_LIST:
        setting = getattr(settings, 'WSAPI_%s' % name, None)
        if setting != None:
            wsapi_settings[name] = setting
    return wsapi_settings


def generate_task_id(**d):
    """
    Generate task id from dict
    """
    result = [str(v) for v in d.values()]
    result.sort()
    md5 = hashlib.md5(''.join(result))
    return md5.hexdigest()


def is_task_done(task_id):
    """
    Returns True if task state in (SUCCESS, FAILURE, IGNORED, REVOKED) or task does not exists
    Also return  True if celery doesn't work properly
    """
    try:
        task = TaskState.objects.get(task_id=task_id)
        if task.state in (
                    states.SUCCESS, states.FAILURE, states.IGNORED,
                                                    states.REVOKED):
            return True
    except TaskState.DoesNotExist:
        return True
    return not is_celery_alive()


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


def decrease_start_date(query):
    """
    Decrease start date by 1 day.
    [NOW-1YEAR TO NOW] -> [NOW-367DAY TO NOW]
    [NOW-2MONTH TO NOW-1MONTH] -> [NOW-63DAY TO NOW-1MONTH]
    [NOW-10DAY TO NOW-3DAY] -> [NOW-11DAY TO NOW-3DAY]
    Works for upload_date, last_modified.
    """
    targets = ('upload_date', 'last_modified',)
    new_query = []
    filters = query.split('&')
    try:
        for f in filters:
            attribute, value = f.split('=')
            if attribute not in targets:
                new_query.append(f)
                continue
            value = urllib.unquote(value)
            first, second = value.split('TO')
            period = first[5:-1]
            days = None
            if 'DAY' in period:
                days = int(period.split('DAY')[0])
            elif 'MONTH' in period:
                days = int(period.split('MONTH')[0]) * 31
            elif 'YEAR' in period:
                days = int(period.split('YEAR')[0]) * 366
            if not days:
                return query
            days += 1
            new_query.append('%s=' % attribute + urllib.quote('[NOW-%dDAY TO%s' % (days, second)))
        return '&'.join(new_query)
    except:
        pass
    return query


# xml processing

def xml_add_spaces(xml, space=0, tab=2):
    """
    Iterator, returns xml with spaces.

    :param xml: input xml
    :param space: initial space
    :param tab: spaces count for one tab
    """
    ELEMENT_START, ELEMENT_STOP, ELEMENT_SINGLE = range(3)
    position = 0
    end_position = 0
    last_element_type = ELEMENT_START
    while end_position != -1:
        # find next element
        start_position = xml.find('<', position)
        end_position = xml.find('>', position)
        element = xml[start_position: end_position + 1]
        # determine element type
        element_type = ELEMENT_START
        if element.find('</') != -1:
            element_type = ELEMENT_STOP
        elif element.find('/>') != -1:
            element_type = ELEMENT_SINGLE
        # decr space if block closed
        if element_type == ELEMENT_STOP:
            space -= tab
        # get block content
        content = xml[position:start_position]
        # add newlines
        if content:
            yield content
        if element_type == ELEMENT_SINGLE:
            yield ' ' * space + element + '\n'
        elif element_type == ELEMENT_STOP:
            if last_element_type == ELEMENT_START:
                yield element + '\n'
            else:
                yield ' ' * space + element + '\n'
        elif last_element_type == ELEMENT_START:
            yield '\n' + ' ' * space + element
        else:
            yield ' ' * space + element
        # incr space if block open
        if element_type == ELEMENT_START:
            space += tab
        position = end_position + 1
        last_element_type = element_type
