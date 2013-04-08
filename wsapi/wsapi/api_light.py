# -*- coding: utf-8 -*-

"""
wsapi.api_light
~~~~~~~~~~~~~~~~~~~~

Implementation of the lightweight way to obtain results from cghub server:
1. obtain ids list for specified query (from cache or load from CGHUB_ANALYSIS_ID_URI)
2. load attributes for specified page items (using CGHUB_ANALYSIS_DETAIL_URI)

"""
import urllib2
import logging
import os
import hashlib
import linecache

from lxml import objectify, etree
from xml.sax import handler, parse, saxutils

from exceptions import QueryRequired

from utils import get_setting


wsapi_request_logger = logging.getLogger('wsapi.request')

# we unable to sort results by this fields at server side
CALCULATED_FIELDS = ('files_size',)


class IDsParser(handler.ContentHandler):
    """
    Content handler class for xml.sax.
    Parse response and save analysis ids to file.
    """

    def __init__(self, filename):
        self.current_element = ''
        self.f = open(filename, 'w')
        handler.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        self.current_element = name

    def endElement(self, name):
        self.current_element = ''

    def characters(self, content):
        if self.current_element in ('Hits', 'analysis_id'):
            self.f.write('%s\n' % content)

    def endDocument(self):
        self.f.close()


def parse_sort_by(value):
    """
    study -> astudy:asc
    -study -> study:desc
    """
    if value[0] == '-':
        return '%s:desc' % value[1:]
    return '%s:asc' % value

def get_cache_file_name(query, settings):
    """
    Calculate cache file name.
    IDs cache files ends with .ids.
    """
    # Prevent getting different file names because of 
    # percent escaping
    query = urllib2.unquote(query.encode("utf8"))
    query = urllib2.quote(query)
    md5 = hashlib.md5(query)
    cache_file_name = u'{0}.ids'.format(md5.hexdigest())
    cache_file_name = os.path.join(
                get_setting('CACHE_DIR', settings),
                cache_file_name)
    return cache_file_name

def load_ids(query, settings):
    """
    Load ids from CGHub server.
    """
    url = u'{0}{1}?{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_ID_URI', settings),
            query)
    wsapi_request_logger.info(urllib2.unquote(url))
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    filename = get_cache_file_name(query, settings)
    cache_dir = get_setting('CACHE_DIR', settings)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    parse(response, IDsParser(filename))

def get_ids(query, offset, limit, settings, sort_by=None, ignore_cache=False):
    """
    Get ids for specified query from cache or load from CGHub server.
    """
    q = query
    if (sort_by and
        not sort_by in CALCULATED_FIELDS and
        not sort_by[1:] in CALCULATED_FIELDS):
        q += '&sort_by=' + parse_sort_by(sort_by)
    filename = get_cache_file_name(q, settings)
    # reload cache if ignore_cache
    if not os.path.exists(filename) or ignore_cache:
        load_ids(q, settings=settings)
    try:
        items_count = int(linecache.getline(filename, 1))
    except ValueError:
        return 0, []
    items = []
    for i in range(offset + 2, offset + limit + 2):
        line = linecache.getline(filename, i).split('\n')[0]
        if line:
            items.append(line)
    linecache.clearcache()
    return items_count, items

def get_all_ids(query, settings, ignore_cache=False):
    """
    Return all ids for specified query.
    Loads them from cghub server or gets from cache if exists
    and ignore_cache == False.

    :param query: a string with query to send to the server
    :param ignore_cache: set to True, to restrict using cached ids
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """
    filename = get_cache_file_name(query, settings)
    # reload cache if ignore_cache
    if not os.path.exists(filename) or ignore_cache:
        load_ids(query, settings=settings)
    f = open(filename)
    try:
        items = f.read().split('\n')[1:-1]
    except:
        return []
    return items

def load_attributes(ids, settings):
    """
    Load attributes for specified set of ids.
    Sorting not implemented for ANALYSIS_DETAIL uri.
    """
    query = 'analysis_id=' + urllib2.quote('(%s)' % ' OR '.join(ids))
    url = u'{0}{1}?{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_DETAIL_URI', settings),
            query)
    wsapi_request_logger.info(urllib2.unquote(url))
    request = urllib2.Request(url)
    response = urllib2.urlopen(request).read()
    results = objectify.fromstring(response)
    return results

def request_light(query, offset, limit, settings, sort_by=None, ignore_cache=False):
    """
    Makes a request to CGHub web service
    or gets data from cache if exists.
    Returns results count and xml for specified page.

    :param query: a string with query to send to the server
    :param offset: offset for results (for paging)
    :param limit: limit (also for paging)
    :param sort_by: sort by this attribute (specify it as ``-date_modified`` to reverse sorting order)
    :param ignore_cache: set to True, to restrict using cached ids
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """

    ids = get_ids(query, offset, limit, sort_by=sort_by,
                            ignore_cache=ignore_cache, settings=settings)
    if ids[0] == 0:
        return ids[0], objectify.fromstring(
            "<ResultSet><Query>%s</Query>"
            "<Hits>0</Hits></ResultSet>" % urllib2.quote(query))
    attributes = load_attributes(ids=ids[1], settings=settings)
    return ids[0], attributes
