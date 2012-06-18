# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import urllib2
import lxml
from lxml import objectify
from django.utils import simplejson as json

from exceptions import QueryRequired


CGHUB_SERVER = 'https://cghub.ucsc.edu'
CGHUB_ANALYSIS_OBJECT_URI = '/cghub/metadata/analysisObject'
CGHUB_ANALYSIS_ATTRIBUTES_URI = '/cghub/metadata/analysisAttributes'



class objectJSONEncoder(json.JSONEncoder):
    """A specialized JSON encoder that can handle simple lxml objectify types
       >>> from lxml import objectify
       >>> obj = objectify.fromstring("<Book><price>1.50</price><author>W. Shakespeare</author></Book>")
       >>> objectJSONEncoder().encode(obj)
       '{"price": 1.5, "author": "W. Shakespeare"}'
    """
    def default(self,o):
        if isinstance(o, lxml.objectify.IntElement):
            return int(o)
        if isinstance(o, lxml.objectify.NumberElement) or isinstance(o, lxml.objectify.FloatElement):
            return float(o)
        if isinstance(o, lxml.objectify.ObjectifiedDataElement):
            return str(o)
        if hasattr(o, '__dict__'):
            #For objects with a __dict__, return the encoding of the __dict__
            return o.__dict__
        return json.JSONEncoder.default(self, o)

def sort_list_of_dictionaries_by(processed_results, sort_by):
    """
    Sorts `lxml.objectify.ObjectifiedElement` by `sort_by`
    """
    reverse_order = False
    if sort_by.startswith("-"):
        reverse_order = True
        sort_by = sort_by[1:]
    
    #from pprint import pprint
    #pprint(processed_results)
    
    sorted_list = sorted(processed_results, key=lambda k: k[sort_by])
    if reverse_order:
        sorted_list.reverse()
    return sorted_list

def request(query=None, file_name=None, sort_by=None):
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
        
    # convert to json
    processed_results = []
    for r in results.Result:
        processed_results.append(json.loads(objectJSONEncoder().encode(r)))
        
    #from pprint import pprint
    #pprint(processed_results)
    #pprint(len(processed_results))
    #assert False, "full_stop"
        
    if sort_by:
        processed_results = sort_list_of_dictionaries_by(processed_results, sort_by)
    #return results
    return processed_results
