import sys
import urllib2
import hashlib
import os
import threading
import socket
import logging

from cghub_python_api import Request
from cghub_python_api.utils import urlopen

from django.conf import settings

from cghub.apps.core.filters_storage import ALL_FILTERS
from cghub.apps.core.attributes import ATTRIBUTES


ALLOWED_ATTRIBUTES = ALL_FILTERS.keys()
api_logger = logging.getLogger('cart')


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


def get_from_test_cache(url, format='xml'):
    """
    Used while testing.
    Trying to get response from cache, if it fails - get response from server and save it to cache.

    :param url: url that passed to urlopen
    :param format: 'xml' or 'json'

    :return: file object
    """
    FORMAT_CHOICES = {
        'xml': 'text/xml',
        'json': 'application/json'
    }
    CACHE_DIR = settings.TEST_CACHE_DIR
    if not os.path.exists(CACHE_DIR) or not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    md5 = hashlib.md5(url)
    path = os.path.join(CACHE_DIR, '%s.%s.cache' % (md5.hexdigest(), format))
    if os.path.exists(path):
        return open(path, 'r')
    headers = {'Accept': FORMAT_CHOICES.get(format, FORMAT_CHOICES['xml'])}
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read()
    with open(path, 'w') as f:
        f.write(content)
    return open(path, 'r')


class APIRequest(Request):

    def patch_input_data(self):
        server_url = getattr(settings, 'CGHUB_SERVER')
        if server_url:
            self.server_url = server_url

    def get_xml_file(self, url):
        if 'test' in sys.argv:
            return get_from_test_cache(url=url)
        api_logger.error(urllib2.unquote(url))
        return urlopen(
                url=url,
                max_attempts=getattr(settings, 'API_HTTP_ERROR_ATTEMPTS', 5),
                sleep_time=getattr(settings, 'API_HTTP_ERROR_SLEEP_AFTER', 1))

    def patch_result(self, result, result_xml):
        new_result = {}
        for attr in ATTRIBUTES:
            if result[attr].exist:
                new_result[attr] = result[attr].text
        new_result['filename'] = result['files.file.0.filename'].text
        try:
            new_result['files_size'] = int(result['files.file.0.filesize'].text)
        except TypeError:
            new_result['files_size'] = 0
        new_result['checksum'] = result['files.file.0.checksum'].text
        return new_result


class RequestIDs(APIRequest):
    """
    Used analysisID uri.
    """

    def patch_input_data(self):
        super(RequestIDs, self).patch_input_data()
        self.uri = self.CGHUB_ANALYSIS_ID_URI


class RequestDetail(APIRequest):
    """
    Used analysisDetail uri.
    """

    def patch_input_data(self):
        super(RequestDetail, self).patch_input_data()
        self.uri = self.CGHUB_ANALYSIS_DETAIL_URI


class RequestFull(APIRequest):
    """
    Used analysisFull uri.
    Raw xml added to results.
    """

    def patch_input_data(self):
        super(RequestFull, self).patch_input_data()
        self.uri = self.CGHUB_ANALYSIS_FULL_URI

    def patch_result(self, result, result_xml):
        new_result = super(RequestFull, self).patch_result(result, result_xml)
        new_result['xml'] = (
                result_xml.replace('\t', '').replace('\n', ''))
        return new_result


class ResultFromFile(RequestFull):
    """
    Allows to create cghub_python_apy.api.Request
    from analysis xml stored in local file
    """

    def get_xml_file(self, url):
        filename = self.query['filename']
        return open(filename, 'r')


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
