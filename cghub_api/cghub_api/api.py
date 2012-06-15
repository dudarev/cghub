# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import urllib2
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
        if not '=' in query:
            raise ValueError("Query seems to be invalid (no '='): %s" % query)
        url = server + uri + '?' + query
        req = urllib2.Request(url)
        response = urllib2.urlopen(req).read()
        results = objectify.fromstring(response)

    return results
