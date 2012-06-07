# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import urllib, urllib2
from lxml import objectify

from exceptions import QueryRequired


CGHUB_SERVER = 'https://cghub.ucsc.edu'
CGHUB_ANALYSIS_OBJECT_URI = '/cghub/metadata/analysisObject'
CGHUB_ANALYSIS_ATTRIBUTES_URI = '/cghub/metadata/analysisAttributes'


def request(query=None, file_name=None):
    """
    Makes a request to CGHub web service or gets data from a file.
    Returns parsed Response object.
    """

    server = CGHUB_SERVER

    if query==None and file_name==None:
        raise QueryRequired

    results = []

    if query==None and file_name:
        results = objectify.fromstring(open(file_name, 'r').read())
    elif query:
        uri = CGHUB_ANALYSIS_ATTRIBUTES_URI
        query_tuple = tuple(query.split('='))
        print len(query_tuple)
        if len(query_tuple) != 2:
            raise ValueError("Invalid field=value pair in query: %s" % query)
        url = server + uri + "?" + urllib.urlencode( [query_tuple] )
        req = urllib2.Request(url)
        response = urllib2.urlopen(req).read()
        results = objectify.fromstring(response)

    return results
