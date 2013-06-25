# -*- coding: utf-8 -*-

"""
wsapi.api
~~~~~~~~~~~~~~~~~~~~

Functions for external use.

"""

import json
import urllib2
import logging

from xml.sax import parse as sax_parse, parseString as sax_parse_string

from .utils import urlopen, prepare_query, get_setting
from .parsers import IDsParser, AttributesParser


wsapi_request_logger = logging.getLogger('wsapi.request')


"""
From WS API documentation:

The querystring may also contain a parameter named ‘sort_by’ whose value is the attribute
by which the results should be sorted. The attribute name may followed by :asc or :desc to
indicate ascending or decending sort order. If ‘sort_by’ is not specified, results are sorted by
‘last_modified’. If no sort order is specified, results are sorted in ascending order.

The querystring may also contain a pagination parameters named start and rows. Parameter
start defines how many results should be skipped and rows defines how many records output
should have.
"""


def add_custom_fields(results):
    """
    Calculate missing fields:
    - files_size
    """
    for result in results:
        files_size = 0
        for f in result['files']:
            files_size += f['filesize']
        result['files_size'] = files_size


def request_page(query, offset=None, limit=None, sort_by=None, settings={}):
    """
    Makes a request to CGHub web service.
    Returns page data in json format.

    :param query: a string with query to send to the server
    :param offset: how many results should be skipped
    :param limit: how many records output should have
    :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """
    query = prepare_query(
                query=query, offset=offset, limit=limit, sort_by=sort_by)
    url = u'{0}{1}?{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_DETAIL_URI', settings),
            query)
    wsapi_request_logger.info(urllib2.unquote(url))
    response = urlopen(url, format='json', settings=settings).read()
    response = json.loads(response)
    hits = int(response['result_set']['hits'])
    results = response['result_set']['results'] if hits else []
    add_custom_fields(results)
    return hits, results


def request_ids(query, sort_by=None, settings={}):
    """
    Returns list of ids for specified query

    :param query: a string with query to send to the server
    :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """
    query = prepare_query(query=query, sort_by=sort_by)
    url = u'{0}{1}?{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_ID_URI', settings),
            query)
    wsapi_request_logger.info(urllib2.unquote(url))
    response = urlopen(url, format='xml', settings=settings)

    hits = 0
    results = []

    def callback(value):
        results.append(value)

    parser = IDsParser(callback)
    sax_parse(response, parser)

    return parser.hits, results


def request_details(query, callback, sort_by=None, settings={}):
    """
    Call callback function for every parsed result. Returns hits.

    :param query: a string with query to send to the server
    :param callback: callable, calls for every parsed result 
    :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """
    query = prepare_query(query=query, sort_by=sort_by)
    url = u'{0}{1}?{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_ID_URI', settings),
            query)
    wsapi_request_logger.info(urllib2.unquote(url))
    response = urlopen(url, format='xml', settings=settings)

    parser = AttributesParser(callback)
    sax_parse(response, parser)

    return parser.hits


def item_details(analysis_id, with_xml=False, settings={}):
    """
    Returns details for file with specified analysis id.

    :param analysis_id: analysis id
    :param with_xml: boolean, result additionally contains raw xml if True
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """
    url = u'{0}{1}/{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_DETAIL_URI', settings),
            analysis_id)
    wsapi_request_logger.info(urllib2.unquote(url))
    if not with_xml:
        content = urlopen(url, format='json', settings).read()
        content = json.loads(content)
        results = content['result_set']['results']
        add_custom_fields(results)
        if results:
            return results[0]
        return {}
    else:
        content = urlopen(url, format='xml', settings).read()
        results = []

        def callback(attributes):
            results.append(attributes)

        sax_parse_string(content, AttributesParser(callback))
        if results:
            result = results[0]
            content = content.replace('\t', '')
            content = content.replace('\n', '')
            result['xml'] = content
            return result
    return {}


def item_xml(analysis_id, with_short=False, settings={}):
    """
    Returns xml for specified analysis id.

    :param analysis_id: analysis id
    :param with_short: boolean, additionally returns item without set of submission metadata if True
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """
    url = u'{0}{1}/{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_FULL_URI', settings),
            analysis_id)
    wsapi_request_logger.info(urllib2.unquote(url))
    xml = urlopen(url, format='xml', settings).read()
    xml = xml.replace('\t', '')
    xml = xml.replace('\n', '')
    if not with_short:
        return xml
    attributes_to_remove = (
            'sample_accession', 'legacy_sample_id',
            'disease_abbr', 'tss_id', 'participant_id', 'sample_id',
            'analyte_code', 'sample_type', 'library_strategy',
            'platform', 'analysis_xml', 'run_xml', 'experiment_xml')
    short_xml = xml
    for attr in attributes_to_remove:
        start = 0
        stop = 0
        while start != -1 and stop != -1:
            start = short_xml.find('<%s>' % attr)
            if start != -1:
                stop = short_xml.find('</%s>' % attr, start)
            if start != -1 and stop != -1:
                short_xml = short_xml[:start] + short_xml[stop + len(attr) + 3:]
    return xml, short_xml
