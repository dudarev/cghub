import os
import threading
import socket

from django.conf import settings

from .filters_storage import ALL_FILTERS
from .requests import RequestDetail


ALLOWED_ATTRIBUTES = ALL_FILTERS.keys()


def get_filters_dict(filters):
    """
    Removes illegal filters from dict.
    """
    filters_dict = {}
    for attr in ALLOWED_ATTRIBUTES:
        if filters.get(attr):
            filters_dict[attr] = filters[attr]
    return filters_dict


def query_dict_to_str(query):
    """
    Transform query dict to string.
    Example:
    query_dict_to_str({'analysis_id': ['123', '345']})
    ->
    'analysis_id=(123 OR 345)'
    """
    parts = []
    for key, value in query.iteritems():
        if isinstance(value, list) or isinstance(value, tuple):
            value_str = ' OR '.join([v for v in value])
            value_str = '(%s)' % value_str.replace('+', ' ')
        else:
            value_str = str(value).replace('+', ' ')
        parts.append('='.join([key, value_str]))
    return '&'.join(parts)


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
    elif settings.PAGINATOR_LIMIT_COOKIE in request.COOKIES:
        limit = str(request.COOKIES[settings.PAGINATOR_LIMIT_COOKIE])
        limit = limit.isdigit() and int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
    else:
        limit = settings.DEFAULT_PAGINATOR_LIMIT
    return offset, limit


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


def makedirs_group_write(path):
    "create a directory, including missing parents, ensuring it has group write permissions"
    old_mask = os.umask(0002)
    try:
        os.makedirs(path)
    finally:
        os.umask(old_mask)


def generate_tmp_file_name():
    """
    Returns filename in next format:
    pid-threadId-host.tmp
    """
    return '{pid}-{thread}-{host}.tmp'.format(
                    pid=os.getpid(), thread=threading.current_thread().name,
                    host=socket.gethostname())


def get_results_for_ids(ids):
    """
    Obtain all necessary attributes for specified analysis_ids
    """
    if not ids:
        return []
    api_request = RequestDetail(query={'analysis_id': ids})
    results = []
    for result in api_request.call():
        results.append(result)
    return results
