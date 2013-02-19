# -*- coding: utf-8 -*-

"""
wsapi.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""
import urllib2

from lxml import objectify, etree
from datetime import datetime

from exceptions import QueryRequired
from cache import get_from_cache, save_to_cache

from settings import (CGHUB_SERVER, CGHUB_ANALYSIS_ID_URI,
                                CGHUB_ANALYSIS_ATTRIBUTES_URI, USE_API_LIGHT)
from api_light import request_light


class Results(object):
    """
    Wrapper class for results obtained with lxml. This object is returned by :func:`request`.
    """

    CALCULATED_FIELDS = ('files_size', 'refassem_short_name',)

    def __init__(self, lxml_results):
        """
        :param lxml_results: needs to be converted with lxml.objectify

        .. code-block :: python

            results = objectify.fromstring(open(cache_file_name, 'r').read())
        """
        self._lxml_results = lxml_results
        self.is_custom_fields_calculated = False
        # used by api_light to specify correct results count
        self.length = 0

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

    def add_custom_fields(self):
        """
        Add files_size and refassem_short_name fields.
        
        Files size is stored in structures

        .. code-block :: xml

            <files>
                <file>
                    ...
                    <filesize></filesize>
                </file>
            </files>

        In real results we see only one file.
        This function takes care of a situation if there will be several ``<file>`` elements.

        Assembly short name is stored in structures

        .. code-block :: xml

            <analysis_xml>
                <ANALYSIS_SET>
                    <ANALYSIS>
                        <ANALYSIS_TYPE>
                            <REFERENCE_ALIGNMENT>
                                <ASSEMBLY>
                                    <STANDARD short_name="GRCh37-lite"/>
                                </ASSEMBLY>
                                ...

        """

        if self.is_custom_fields_calculated:
            return
        if not hasattr(self, 'Result'):
            return
        for r in self.Result:
            files_size = 0
            for f in r.files.file:
                files_size += int(f.filesize)
            r.files_size = files_size
            r.refassem_short_name = r.analysis_xml.ANALYSIS_SET\
                    .ANALYSIS.ANALYSIS_TYPE.REFERENCE_ALIGNMENT\
                    .ASSEMBLY.STANDARD.get('short_name')
        self.is_custom_fields_calculated = True

    def sort(self, sort_by):
        """
        Sorts results by attribute ``sort_by``.
        If ``sort_by`` starts with ``-`` the order is descending.
        If ``sort_by`` is ``files_size`` it is calculated. See :py:meth:`add_custom_fields` for details.
        """
        from operator import itemgetter

        # figure out order
        reverse_order = False
        if sort_by.startswith("-"):
            reverse_order = True
            sort_by = sort_by[1:]

        if sort_by in self.CALCULATED_FIELDS:
            self.add_custom_fields()

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
        attributes_to_remove = [
            'sample_accession', 'legacy_sample_id',
            'disease_abbr', 'tss_id', 'participant_id', 'sample_id',
            'analyte_code', 'sample_type', 'library_strategy',
            'platform', 'analysis_xml', 'run_xml', 'experiment_xml', ]
        for r in self.Result:
            for a in attributes_to_remove:
                r.remove(r.find(a))
            r.analysis_attribute_uri = \
                CGHUB_SERVER + CGHUB_ANALYSIS_ATTRIBUTES_URI + '/' + r.analysis_id
            objectify.deannotate(r.analysis_attribute_uri)
            etree.cleanup_namespaces(r)


def merge_results(xml_results):
    """
    Merges search results into one object.

    Iterable may contain instances of (even at the same time):

    :class:`lxml.objectify.ObjectifiedElement`
        Make sure it has Query, Hits attributes(may not contain Result attribute)
    :class:`wsapi.api.Results`
        Its attribute _lxml_results must meet requirements above

    Merging excludes duplicates. Timestamp is added after merging.
    Queries are aggregated.

    Returns lxml.objectify.ObjectifiedElement instance containing merged xml data.
    """
    if not isinstance(xml_results, tuple) and not isinstance(xml_results, list):
        raise Exception('xml_results must be tuple or list')

    if not xml_results:
        raise Exception('Nothing to merge!')

    result = objectify.XML('<ResultSet></ResultSet>')
    # list of already merged id
    merged_ids = []
    counter = 1

    for xml_result in xml_results:
        # In case of element is instance of wsapi.api.Results class
        if hasattr(xml_result, '_lxml_results'):
            xml = xml_result._lxml_results
        else:
            xml = xml_result

        if hasattr(xml, 'Result'):
            for r in xml.Result:
                if not r.analysis_id in merged_ids:
                    r.set('id', str(counter))
                    counter += 1
                    result.append(r)
        result.insert(0, xml.Query)
        # renew list of merged ids
        merged_ids = result.xpath('/ResultSet/Result/analysis_id')

    hits = 0
    try:
        hits = len(result.Result)
    except AttributeError:
        pass
    result.insert(0, objectify.fromstring('<Hits>%d</Hits>' % hits))
    result.set('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return result


def request(
        query=None, offset=None, limit=None, sort_by=None,
        get_attributes=True, file_name=None, ignore_cache=False,
                                                use_api_light=False):
    """
    Makes a request to CGHub web service or gets data from a file.
    Returns parsed :class:`wsapi.api.Results` object.

    If file_name specified reads results from file.
    Else tries to get results from cache.
    Else tries to get results from the server.
    Then caches the results if needed and returns sorted results.

    :param query: a string with query to send to the server
    :param offset: offset for results (for paging)
    :param limit: limit (also for paging)
    :param sort_by: sort by this attribute (specify it as ``-date_modified`` to reverse sorting order)
    :param get_attributes: boolean to get results with attributes or not (``True`` by default), see :ref:`wsi-api` for details
    :param file_name: only this parameter maybe specified, in this case results are obtained from a file
    :param use_api_light: use api_light to obtain results, it works more efficient with large queries
    """

    if use_api_light and USE_API_LIGHT:
        hits, results = request_light(
                            query=query,
                            offset=offset or 0,
                            limit=limit or 10,
                            sort_by=sort_by,
                            ignore_cache=ignore_cache)
        results = Results(results)
        if sort_by:
            results.sort(sort_by)
        results.length = hits
        return results

    results = []
    results_from_cache = True

    if query is None and file_name is None:
        raise QueryRequired

    if query is None and file_name:
        results = objectify.fromstring(open(file_name, 'r').read())

    # Getting results from the cache
    if not len(results) and not ignore_cache:
        results, cache_errors = get_from_cache(
            query=query, get_attributes=get_attributes)

    # Getting results from the server
    if not len(results):
        results_from_cache = False
        server = CGHUB_SERVER
        if get_attributes:
            uri = CGHUB_ANALYSIS_ATTRIBUTES_URI
        else:
            uri = CGHUB_ANALYSIS_ID_URI
        if not '=' in query:
            raise ValueError("Query seems to be invalid (no '='): %s" % query)
        url = u'{0}{1}?{2}'.format(server, uri, query)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req).read()
        results = objectify.fromstring(response)

    # wrap result with extra methods
    results = Results(results)

    # Saving results to the cache
    if not ignore_cache and not results_from_cache:
        save_to_cache(query=query, get_attributes=get_attributes, data=results)

    # Sort and slice if needed
    if hasattr(results, 'Result'):
        if sort_by:
            results.sort(sort_by=sort_by)
        if offset or limit:
            offset = offset or 0
            limit = limit or 0
            if isinstance(results.Result, (list, tuple)):
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


def multiple_request(
        queries_list=None, offset=None, limit=None, sort_by=None,
        get_attributes=True, file_name=None, ignore_cache=False):
    """
    The only difference from wsapi.api.request is that the first argument can be
    iterable(tuple or list) with many queries.

    If takes string as first argument acts like request().

    Returns :class:`wsapi.api.Results` instance
    """

    if isinstance(queries_list, str):
        return request(
            queries_list, offset, limit, sort_by,
            get_attributes, file_name, ignore_cache, use_api_light=True)

    if not isinstance(queries_list, tuple) and not isinstance(queries_list, list):
        raise Exception('The first argument must be tuple or list')

    results = []
    results_from_cache = True

    if not queries_list and file_name is None:
        raise QueryRequired

    if not queries_list and file_name:
        results = objectify.fromstring(open(file_name, 'r').read())

    # Getting results from the cache
    if not len(results) and not ignore_cache:
        results, cache_errors = get_from_cache(
            query=str(list(queries_list)), get_attributes=get_attributes)

    if not len(results):
        results_from_cache = False
        results_list = []
        for query in queries_list:
            results_list.append(
                request(
                    query=query, offset=None, limit=None, sort_by=None,
                    get_attributes=get_attributes, file_name=file_name, ignore_cache=ignore_cache))
        results = merge_results(results_list)

    results = Results(results)

    # Saving results to the cache
    if not ignore_cache and not results_from_cache:
        save_to_cache(query=str(list(queries_list)), get_attributes=get_attributes, data=results)

    # Sort and slice if needed
    if hasattr(results, 'Result'):
        if sort_by:
            results.sort(sort_by=sort_by)
        if offset or limit:
            offset = offset or 0
            limit = limit or 0
            if isinstance(results.Result, (list, tuple)):
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
