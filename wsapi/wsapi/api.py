# -*- coding: utf-8 -*-

"""
wsapi.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import os
import urllib2
import hashlib

from lxml import objectify, etree

from exceptions import QueryRequired
from settings import CACHE_DIR

CGHUB_SERVER = 'https://cghub.ucsc.edu'
CGHUB_ANALYSIS_OBJECT_URI = '/cghub/metadata/analysisObject'
CGHUB_ANALYSIS_ATTRIBUTES_URI = '/cghub/metadata/analysisAttributes'


class Results(object):
    """
    Wrapper class for results obtained with lxml. This object is returned by :func:`request`.
    """
    def __init__(self, lxml_results):
        """
        :param lxml_results: needs to be converted with lxml.objectify

        .. code-block :: python

            results = objectify.fromstring(open(cache_file_name, 'r').read())
        """
        self._lxml_results = lxml_results
        self.is_files_size_calculated = False

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._lxml_results, attr)

    def __getitem__(self, item):
        return self[item]

    @classmethod
    def from_file(cls, file_name):
        """
        Initialize :class:`Results <Results>` from a file.
        """
        with open(file_name) as f:
            return cls(
                    objectify.fromstring(
                        f.read()
                        )
                    )

    def calculate_files_size(self):
        """Files size is stored in structures

        .. code-block :: xml

            <files>
                <file>
                    ...
                    <filesize></filesize>
                </file>
            </files>

        In real results we see only one file.
        This function takes care of a situation if there will be several ``<file>`` elements.
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
        Sorts results by attribute ``sort_by``.
        If ``sort_by`` starts with ``-`` the order is descending.
        If ``sort_by`` is ``files_size`` it is calculated. See :py:meth:`calculate_files_size` for details.
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
        """
        Converts object to a string.
        """
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
    Returns parsed :class:`Results` object.

    :param query: a string with query to send to the server
    :param offset: offset for results (for paging)
    :param limit: limit (also for paging)
    :param sort_by: sort by this attribute (specify it as ``-date_modified`` to reverse sorting order)
    :param get_attributes: boolean to get results with attributes or not (``True`` by default), see :ref:`wsi-api` for details
    :param file_name: only this parameter maybe specified, in this case results are obtained from a file
    """

    # see if cache file exists
    if query:
        m = hashlib.md5()
        m.update(query)
        cache_file_name = u'{0}.xml'.format(m.hexdigest())
        if not get_attributes:
            cache_file_name = cache_file_name + '-no-attr'
        cache_file_name = os.path.join(CACHE_DIR, cache_file_name)

    results = []
    xml_syntax_error_raised = False
    if query and os.path.exists(cache_file_name):
        try:
            results = objectify.fromstring(open(cache_file_name, 'r').read())
        except etree.XMLSyntaxError:
            xml_syntax_error_raised = True

    if not results:
        server = CGHUB_SERVER

        if query == None and file_name == None:
            raise QueryRequired

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

    # save results to cache if it was a query and cache did not exists
    if query and (xml_syntax_error_raised or not os.path.exists(cache_file_name)):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        f = open(cache_file_name, 'w')
        f.write(results.tostring())
        f.close()

    # sort and slice if needed
    if hasattr(results, 'Result'):
        if sort_by:
            results.sort(sort_by=sort_by)
        if offset or limit:
            offset = offset or 0
            limit = limit or 0
            if isinstance(results.Result, (list,tuple)):
                results.Result = results.Result[offset:offset + limit]
            else:
                result_all = results.findall('Result')
                idx_from = results.index(result_all[0])
                for r in result_all:
                    results.remove(r)
                cslice = result_all[offset:offset + limit]
                for i, c in enumerate(cslice):
                    results.insert(i + idx_from, c)


    return results
