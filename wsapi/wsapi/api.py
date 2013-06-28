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
from .exceptions import QueryRequired


wsapi_request_logger = logging.getLogger('wsapi.request')


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

    :return: (hits, results). hits - count of results found, results - results list (limited by limit param)
    """
    if query is None:
        raise QueryRequired
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
    Makes a request to CGHub web service.
    Returns list of ids for specified query

    :param query: a string with query to send to the server
    :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
    :param settings: custom settings, see `wsapi.settings.py` for settings example

    :return: (hits, results). hits - count of results found, results - list of results found
    """
    if query is None:
        raise QueryRequired
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
    Makes a request to CGHub web service.
    Call callback function for every parsed result. Returns hits.

    :param query: a string with query to send to the server
    :param callback: callable, calls for every parsed result 
    :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
    :param settings: custom settings, see `wsapi.settings.py` for settings example

    :return: hits - count of results found
    """
    if query is None:
        raise QueryRequired
    query = prepare_query(query=query, sort_by=sort_by)
    url = u'{0}{1}?{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_DETAIL_URI', settings),
            query)
    wsapi_request_logger.info(urllib2.unquote(url))
    response = urlopen(url, format='xml', settings=settings)
    parser = AttributesParser(callback)
    sax_parse(response, parser)

    return parser.hits


def item_details(analysis_id, with_xml=False, settings={}):
    """
    Makes a request to CGHub web service.
    Returns details for file with specified analysis id.

    :param analysis_id: analysis id
    :param with_xml: boolean, result additionally contains raw xml if True
    :param settings: custom settings, see `wsapi.settings.py` for settings example

    :return: dict filled by item attributes if found, else - empty dict
    """
    url = u'{0}{1}/{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_DETAIL_URI', settings),
            analysis_id)
    wsapi_request_logger.info(urllib2.unquote(url))
    if not with_xml:
        content = urlopen(url, format='json', settings=settings).read()
        content = json.loads(content)
        results = content['result_set']['results']
        add_custom_fields(results)
        if results:
            return results[0]
        return {}
    else:
        content = urlopen(url, format='xml', settings=settings).read()
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
    Makes a request to CGHub web service.
    Returns xml for specified analysis id.

    :param analysis_id: analysis id
    :param with_short: boolean, additionally returns item without set of submission metadata if True
    :param settings: custom settings, see `wsapi.settings.py` for settings example

    :return: xml string or (xml string, shortened xml string) if with_short==True
    """
    url = u'{0}{1}/{2}'.format(
            get_setting('CGHUB_SERVER', settings),
            get_setting('CGHUB_ANALYSIS_FULL_URI', settings),
            analysis_id)
    wsapi_request_logger.info(urllib2.unquote(url))
    xml = urlopen(url, format='xml', settings=settings).read()
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
