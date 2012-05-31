# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import xml.dom.minidom

from exceptions import QueryRequired

import experiment 

def request(query=None, file_name=None):
    """
    Makes a request to CGHub web service or gets data from a file.
    Returns parsed Response object.
    """

    if query==None and file_name==None:
        raise QueryRequired

    results = []

    if query==None and file_name:
        f = open(file_name, 'r')
        raw_xml = f.read()
        dom = xml.dom.minidom.parseString(raw_xml)
        results_dom = dom.getElementsByTagName('Result')
        results = []
        for r in results_dom:
            experimentTag = r.getElementsByTagName('experiment_xml')[0].firstChild
            dom_instance = experiment.CreateFromDOM(experimentTag)
            results.append(dom_instance)
            
    return results
