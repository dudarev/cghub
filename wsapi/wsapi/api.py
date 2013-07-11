# -*- coding: utf-8 -*-

"""
wsapi.api
~~~~~~~~~~~~~~~~~~~~

Code for external use.

"""

import json
import urllib2
import logging

from xml.sax import parse as sax_parse, parseString as sax_parse_string

from .utils import urlopen, prepare_query, get_setting
from .parsers import IDsParser, AttributesParser
from .exceptions import QueryRequired


wsapi_request_logger = logging.getLogger('wsapi.request')


class Request(object):

    def __init__(
                self, query, only_ids=False, full=False, with_xml=False,
                offset=None, limit=None, sort_by=None, callback=None,
                                                        settings={}):
        """
        :param query: a string with query to send to the server
        :param only_ids: boolean, only ids will be returned in result, will be used analysisId uri
        :param full: boolean, if True, will be used analysisFull uri, otherwise - analysisDetail uri
        :param with_xml: boolean, self.xml will be filled by response xml if True
        :param offset: how many results should be skipped
        :param limit: how many records output should have
        :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
        :param callback: callable, calls for every parsed result if specified (in this case self.results will be empty)
        :param settings: custom settings, see `wsapi.settings.py` for settings example
        """
        if query is None:
            raise QueryRequired
        if only_ids:
            self.parser_class = IDsParser
            self.uri = get_setting('CGHUB_ANALYSIS_ID_URI', settings)
        else:
            self.parser_class = AttributesParser
            if full:
                self.uri = get_setting('CGHUB_ANALYSIS_FULL_URI', settings)
            else:
                self.uri = get_setting('CGHUB_ANALYSIS_DETAIL_URI', settings)
        self.query = query
        self.with_xml = with_xml
        self.only_ids = only_ids
        self.limit = limit
        self.offset = offset
        self.sort_by = sort_by
        self.callback = callback
        self.settings = settings

        self.results = []
        self.hits = 0
        self.xml = ''

        self._get_data()

    def patch_result(self, result):
        """
        May be overridden to add some custom fields to results
        """
        return result

    def _process_result(self, result):
        if not self.only_ids:
            result = dict(self.patch_result(result))
        if self.callback:
            self.callback(result)
        else:
            self.results.append(result)

    def _get_data(self):
        query = prepare_query(
                    query=self.query, offset=self.offset,
                    limit=self.limit, sort_by=self.sort_by)
        url = u'{0}{1}?{2}'.format(
                    get_setting('CGHUB_SERVER', self.settings),
                    self.uri, query)
        wsapi_request_logger.info(urllib2.unquote(url))

        parser = self.parser_class(self._process_result)
        if self.with_xml:
            response = urlopen(
                        url, format='xml', settings=self.settings).read()
            self.xml = response.replace('\t', '')
            self.xml = self.xml.replace('\n', '')
            sax_parse_string(response, parser)
        else:
            response = urlopen(url, format='xml', settings=self.settings)
            sax_parse(response, parser)

        self.hits = parser.hits
