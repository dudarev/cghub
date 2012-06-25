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


def sort_results(results, sort_by):
    """
    Sorts results list by sort_by attribute
    """
    from operator import itemgetter

    reverse_order = False
    
    # figure out order
    if sort_by.startswith("-"):
        reverse_order = True
        sort_by = sort_by[1:]
    
    try:
        sorted_list = sorted(results, key=itemgetter(sort_by))
    except AttributeError:
        # no such child, return original unsorted result
        return results
    
    # reverse order if needed
    if reverse_order:
        sorted_list.reverse()
    return sorted_list

def request(query=None, file_name=None, sort_by=None, get_attributes=True):
    """
    Makes a request to CGHub web service or gets data from a file.
    Returns parsed Response object.
    """

    server = CGHUB_SERVER

    if query == None and file_name == None:
        raise QueryRequired

    results = []

    if query == None and file_name:
        results = objectify.fromstring(open(file_name, 'r').read())
    elif query:
        if get_attributes:
            uri = CGHUB_ANALYSIS_ATTRIBUTES_URI
        else:
            uri = CGHUB_ANALYSIS_OBJECT_URI
        if not '=' in query:
            raise ValueError("Query seems to be invalid (no '='): %s" % query)
        url = server + uri + '?' + query
        req = urllib2.Request(url)
        response = urllib2.urlopen(req).read()
        results = objectify.fromstring(response)

    if hasattr(results, 'Result'):
        # convert objectified results to list and preserve all parent leafs
        results.Result = [x for x in results.Result]

    # sort if needed
    if hasattr(results, 'Result') and sort_by:
        results.Result = sort_results(results.Result, sort_by)

    return results
