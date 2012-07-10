# -*- coding: utf-8 -*-

"""
cghub_api.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import os
import urllib2
import hashlib

from lxml import objectify, etree

from exceptions import QueryRequired


CGHUB_SERVER = 'https://cghub.ucsc.edu'
CGHUB_ANALYSIS_OBJECT_URI = '/cghub/metadata/analysisObject'
CGHUB_ANALYSIS_ATTRIBUTES_URI = '/cghub/metadata/analysisAttributes'

CACHE_DIR = '/tmp/cghub_api/'


class Results(object):
    """
    Wrapper class for results obtained with lxml.
    """
    def __init__(self, lxml_results):
        self._lxml_results = lxml_results
        self.is_files_size_calculated = False

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._lxml_results, attr)

    def __getitem__(self, item):
        return self[item]

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
        if not hasattr(self, 'Result'):
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
    
    def tostring(self):
        return etree.tostring(self._lxml_results)

    def remove_attributes(self):
        """
        Removes some attributes from results to make them shorter.
        """
        attributes_to_remove = ['sample_accession', 'legacy_sample_id', 
                'disease_abbr', 'tss_id', 'participant_id', 'sample_id',
                'analyte_code', 'sample_type', 'library_strategy',
                'platform', 'analysis_xml', 'run_xml', 'experiment_xml',]
        for r in self.Result:
            for a in attributes_to_remove:
                r.remove(r.find(a))
            r.analysis_attribute_uri = \
                CGHUB_SERVER + CGHUB_ANALYSIS_ATTRIBUTES_URI + '/' + r.analysis_id
            objectify.deannotate(r.analysis_attribute_uri)
            etree.cleanup_namespaces(r)


def request(query=None, offset=None, limit=None, sort_by=None, get_attributes=True, file_name=None):
    """
    Makes a request to CGHub web service or gets data from a file.
    Returns parsed Response object.
    """

    # see if cache file exists
    if query:
        m = hashlib.md5()
        m.update(query)
        cache_file_name = u'{0}.xml'.format(m.hexdigest())
        cache_file_name = os.path.join(CACHE_DIR, cache_file_name)

    if query and os.path.exists(cache_file_name):
        results = objectify.fromstring(open(cache_file_name, 'r').read())

    else:
    
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

    # wrap result with extra methods
    results = Results(results)

    # sort if needed
    if hasattr(results, 'Result') and sort_by:
        results.sort(sort_by=sort_by)

    results.Result = results[offset:limit]

    return results
