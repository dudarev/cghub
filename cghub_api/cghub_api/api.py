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


class Results(object):
    '''
    Wrapper class for results obtained with lxml.
    '''
    def __init__(self, lxml_results):
        self._lxml_results = lxml_results
        self.is_files_size_calculated = False

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._lxml_results, attr)

    def calculate_files_size(self):
        """
        Files size is stored in structures
            <files>
                <file>
                    ...
                    <filesize></filesize>
                </file>
            </files>
        In real results we see only one file.
        This function takes care of a situation if there will be several <file>
        """
        if self.is_files_size_calculated:
            return
        for r in self.Result:
            files_size = 0
            for f in r.files.file:
                files_size += int(f.filesize)
            r.files_size = files_size
        self.is_files_size_calculated = True

    def sort(self, sort_by):
        """
        If sort_by starts with "-" the order is descending.
        """
        from operator import itemgetter

        # figure out order
        reverse_order = False
        if sort_by.startswith("-"):
            reverse_order = True
            sort_by = sort_by[1:]
        
        if sort_by == 'files_size':
            self.calculate_files_size()

        self.Result = [x for x in self.Result]

        try:
            self.Result.sort(key=itemgetter(sort_by), reverse=reverse_order)
        except AttributeError:
            # no such child, return original unsorted result
            return


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
        url = u'{0}{1}?{2}'.format(server, uri, query)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req).read()
        results = objectify.fromstring(response)

    if hasattr(results, 'Result'):
        # convert objectified results to list and preserve all parent leafs
        results.Result = [x for x in results.Result]

    # sort if needed
    if hasattr(results, 'Result') and sort_by:
        results.Result = sort_results(results.Result, sort_by)

    return Results(results)
