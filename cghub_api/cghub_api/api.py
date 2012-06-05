# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
from lxml import objectify

from exceptions import QueryRequired


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
