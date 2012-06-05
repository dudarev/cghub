# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import xml.dom.minidom
from lxml import objectify, etree

from exceptions import QueryRequired

import experiment 
import analysis

class Result(object):
    experiment_xml = None
    analysis_xml = None
    pass

def request(query=None, file_name=None):
    """
    Makes a request to CGHub web service or gets data from a file.
    Returns parsed Response object.
    """

    if query==None and file_name==None:
        raise QueryRequired

    results = []

    if query==None and file_name:
        results = objectify.fromstring(open(file_name, 'r').read())
            
    return results
