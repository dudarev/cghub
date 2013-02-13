# -*- coding: utf-8 -*-

"""
wsapi.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import urllib2
import os
import hashlib
import linecache
import datetime

from lxml import objectify, etree
from xml.sax import handler, parse, saxutils

from exceptions import QueryRequired
from settings import (CGHUB_SERVER, CGHUB_ANALYSIS_ID_URI,
                                CGHUB_ANALYSIS_ATTRIBUTES_URI, CACHE_DIR)


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


def get_cache_file_name(query):
    # Prevent getting different file names because of 
    # percent escaping
    query = urllib2.unquote(query.encode("utf8"))
    query = urllib2.quote(query)
    md5 = hashlib.md5(query)
    cache_file_name = u'{0}_ids.xml'.format(md5.hexdigest())
    cache_file_name = os.path.join(CACHE_DIR, cache_file_name)
    print 'nanvel >>> filename ==', cache_file_name
    return cache_file_name

def load_ids(query):
    url = u'{0}{1}?{2}'.format(CGHUB_SERVER, CGHUB_ANALYSIS_ID_URI, query)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    filename = get_cache_file_name(query)
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    parse(response, IDsParser(filename))

def get_ids(query, offset, limit, sort_by=None, ignore_cache=False):
    q = query
    if sort_by and not sort_by in CALCULATED_FIELDS:
        q += '&sort_by=%s' % urllib.quote(sort_by)
    filename = get_cache_file_name(q)
    # reload cache if ignore_cache
    if not os.path.exists(filename) or ignore_cache:
        load_ids(query)
    items_count = int(linecache.getline(filename, 1))
    items = []
    for i in range(offset + 2, offset + limit + 2):
        line = linecache.getline(filename, i)[:-1]
        if line:
            items.append(line)
    linecache.clearcache()
    return items_count, items

def load_attributes(ids):
    query = 'analysis_id=' + urllib2.quote('(%s)' % ' OR '.join(ids))
    url = u'{0}{1}?{2}'.format(CGHUB_SERVER, CGHUB_ANALYSIS_ATTRIBUTES_URI, query)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request).read()
    results = objectify.fromstring(response)
    return results

def request_lightweight(query, offset, limit, sort_by=None, ignore_cache=False):
    """
    Makes a request to CGHub web service or gets data from a file.
    Returns results count and xml for first page.

    :param query: a string with query to send to the server
    :param offset: offset for results (for paging)
    :param limit: limit (also for paging)
    :param sort_by: sort by this attribute (specify it as ``-date_modified`` to reverse sorting order)
    :ignore_cache: set to True, to restrict using cached ids
    """

    ids = get_ids(query, offset, limit, sort_by=None, ignore_cache=ignore_cache)
    if ids[0] == 0:
        return ids[0], objectify.fromstring(
            "<ResultSet><Query>%s</Query>"
            "<Hits>0</Hits></ResultSet>" % urllib2.quote(query))
    attributes = load_attributes(ids[1])
    return ids[0], attributes

"""
Usage:
        hits, results = request_lightweight(
                            query=query,
                            offset=offset or 0,
                            limit=limit or 10,
                            sort_by=sort_by,
                            ignore_cache=ignore_cache)
        results = Results(results)
        results.length = hits
"""
