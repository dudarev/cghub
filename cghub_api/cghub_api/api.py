# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import xml.dom.minidom
from lxml import objectify

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
        f = open(file_name, 'r')
        raw_xml = f.read()
        dom = xml.dom.minidom.parseString(raw_xml)
        results_dom = dom.getElementsByTagName('Result')
        results = []
        for r in results_dom:
            t = Result()
            experimentTag = r.getElementsByTagName('experiment_xml')[0].firstChild
            dom_instance = experiment.CreateFromDOM(experimentTag)
            t.experiment_xml = dom_instance
            analysisTag = r.getElementsByTagName('analysis_xml')[0]
            dom_instance = objectify.XML(analysisTag.toxml())
            print dir(dom_instance)
            print dom_instance.ANALYSIS_SET.ANALYSIS[0].TITLE
            t.analysis_xml = dom_instance
            results.append(t)
            
    return results
