import codecs
import datetime
import logging
import os
import re
import sys
import urllib2
import hashlib

from cghub_python_api import WSAPIRequest, SOLRRequest
from cghub_python_api.utils import urlopen

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .attributes import ATTRIBUTES, SORT_BY_ATTRIBUTES
from .templatetags.search_tags import file_size as file_size_to_str
from .utils import makedirs_group_write


if settings.API_TYPE == 'WSAPI':
    REQUEST_CLASS = WSAPIRequest
elif settings.API_TYPE == 'SOLR':
    REQUEST_CLASS = SOLRRequest


api_logger = logging.getLogger('api.request')


def get_from_test_cache(url, format='xml'):
    """
    Used while testing.
    Trying to get response from cache, if it fails - get response from server and save it to cache.

    :param url: url that passed to urlopen
    :param format: 'xml' or 'json'

    :return: file object
    """
    FORMAT_CHOICES = {
        'xml': 'text/xml',
        'json': 'application/json'
    }
    CACHE_DIR = settings.TEST_CACHE_DIR
    if not os.path.exists(CACHE_DIR) or not os.path.isdir(CACHE_DIR):
        makedirs_group_write(CACHE_DIR)
    md5 = hashlib.md5(url)
    path = os.path.join(CACHE_DIR, '%s_%s.%s.cache' % (
            settings.API_TYPE.lower(), md5.hexdigest(), format))
    if os.path.exists(path):
        if format == 'json':
            return open(path, 'r')
        else:
            return codecs.open(path, 'r', encoding='utf-8')
    headers = {'Accept': FORMAT_CHOICES.get(format, FORMAT_CHOICES['xml'])}
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read()
    if format == 'json':
        # JSON is always ASCII and uses \uXXXX to represent non-ASCII symbols.
        with open(path, 'w') as f:
            f.write(content)
        return open(path, 'r')
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return codecs.open(path, 'r', encoding='utf-8')


def build_wsapi_xml(result):
    """
    Makes solr xml response the same as wsapi response.
    <str name="analysis_id"> -> <analysis_id>, etc.
    """
    files_count = 0
    files_size = 0
    files = []
    for i in range(10):
        if result['filename.%s' % i].text == None:
            break
        files.append({
            'filename': result['filename.%s' % i].text,
            'filesize': result['filesize.%s' % i].text,
            'checksum': result['checksum.%s' % i].text,
            'checksum_method': result['checksum_method.%s' % i].text,
            })
        files_count += 1
        files_size += int(result['filesize.%s' % i].text)
    size_str = file_size_to_str(files_size)
    try:
        files_size, files_units = size_str.split(' ')
        files_size = files_size.replace(',', '.')
    except ValueError:
        files_size = '0'
        files_units = 'KB'
    xml = render_to_string('xml/wsapi_response.xml', {
            'timestamp': datetime.datetime.strftime(
                    timezone.now(), '%Y-%m-%d %H:%M:%S'),
            'result': result,
            'files': files,
            'files_count': files_count,
            'files_size': files_size,
            'files_units': files_units,
            'server_url': settings.CGHUB_DOWNLOAD_SERVER})
    return xml


class RequestBase(REQUEST_CLASS):

    def patch_input_data(self):
        server_url = getattr(settings, 'CGHUB_SERVER', None)
        if server_url:
            self.server_url = server_url
        if settings.API_TYPE == 'SOLR':
            # set SOLR uri if specified
            self.uri = getattr(settings, 'CGHUB_SERVER_SOLR_URI', self.uri)
        # filter sort_by
        if self.sort_by:
            if self.sort_by.find('-') == 0:
                if self.sort_by[1:] not in SORT_BY_ATTRIBUTES:
                    self.sort_by = None
            else:
                if self.sort_by not in SORT_BY_ATTRIBUTES:
                    self.sort_by = None
        # patch for preservation_method filter
        # ffpe: xml_text:("EXPERIMENT_ATTRIBUTE TAG SAMPLE_PRESERVATION TAG VALUE FFPE")
        # frozen: -xml_text:("EXPERIMENT_ATTRIBUTE TAG SAMPLE_PRESERVATION TAG VALUE FFPE")
        if 'preservation_method' in self.query:
            if 'ffpe' in self.query['preservation_method']:
                if 'xml_text' in self.query:
                    if isinstance(self.query['xml_text'], list):
                        pass
                    elif isinstance(self.query['xml_text'], tuple):
                        self.query['xml_text'] = list(self.query['xml_text'])
                    else:
                        self.query['xml_text'] = [str(self.query['xml_text'])]
                else:
                    self.query['xml_text'] = []
                self.query['xml_text'].append('EXPERIMENT_ATTRIBUTE TAG SAMPLE_PRESERVATION TAG VALUE FFPE')
            elif 'frozen' in self.query['preservation_method']:
                if '-xml_text' in self.query:
                    if isinstance(self.query['-xml_text'], list):
                        pass
                    elif isinstance(self.query['-xml_text'], tuple):
                        self.query['-xml_text'] = list(self.query['-xml_text'])
                    else:
                        self.query['-xml_text'] = [str(self.query['-xml_text'])]
                else:
                    self.query['-xml_text'] = []
                self.query['-xml_text'].append('EXPERIMENT_ATTRIBUTE TAG SAMPLE_PRESERVATION TAG VALUE FFPE')
            del self.query['preservation_method']

    def get_source_file(self, url):
        if 'test' in sys.argv:
            return get_from_test_cache(url=url, format=self.format)
        api_logger.debug(urllib2.unquote(url))
        return urlopen(
                url=url,
                format=self.format,
                max_attempts=getattr(settings, 'API_HTTP_ERROR_ATTEMPTS', 5),
                sleep_time=getattr(settings, 'API_HTTP_ERROR_SLEEP_AFTER', 1))

    def patch_result(self, result, result_xml):
        new_result = {}
        for attr in ATTRIBUTES:
            if result[attr].exist:
                new_result[attr] = result[attr].text
        # files
        new_result['files'] = []
        for i in range(10):
            if not result['filename.%d' % i].exist:
                break
            new_result['files'].append({
                'filename': result['filename.%d' % i].text,
                'filesize': int(result['filesize.%d' % i].text),
                'checksum': result['checksum.%d' % i].text,
            })
        try:
            new_result['filename'] = new_result['files'][0]['filename']
            new_result['checksum'] = new_result['files'][0]['checksum']
            new_result['files_size'] = new_result['files'][0]['filesize']
        except KeyError:
            new_result['filename'] = ''
            new_result['checksum'] = ''
            new_result['files_size'] = 0
        return new_result


class RequestID(RequestBase):
    """
    URI: analysisID uri.
    Fields: analysis_id.
    """

    def patch_input_data(self):
        super(RequestID, self).patch_input_data()
        self.uri = getattr(self, 'CGHUB_ANALYSIS_ID_URI', self.uri)
        self.fields = ['analysis_id']

    def patch_result(self, result, result_xml):
        return {'analysis_id': result['analysis_id'].text}


class RequestMinimal(RequestBase):
    """
    URI: analysisDetail uri.
    Fields: analysis_id, last_modified.
    """

    def patch_input_data(self):
        super(RequestMinimal, self).patch_input_data()
        self.uri = getattr(self, 'CGHUB_ANALYSIS_DETAIL_URI', self.uri)
        self.fields = ['analysis_id', 'last_modified']

    def patch_result(self, result, result_xml):
        return {
                'analysis_id': result['analysis_id'].text,
                'last_modified': result['last_modified'].text}


class RequestDetail(RequestBase):
    """
    URI: analysisDetail uri.
    Fields: analysis_id, state, reason, last_modified,
            upload_date, published_date, center_name, study,
            aliquot_id, filename, filesize, checksum,
            sample_accession, legacy_sample_id, disease_abbr,
            tss_id, participant_id, sample_id, analyte_code,
            sample_type, library_strategy, platform,
            refassem_short_name
    """

    def patch_input_data(self):
        super(RequestDetail, self).patch_input_data()
        self.uri = getattr(self, 'CGHUB_ANALYSIS_DETAIL_URI', self.uri)
        self.fields = [
            'analysis_id', 'state', 'reason', 'last_modified',
            'upload_date', 'published_date', 'center_name', 'study',
            'aliquot_id', 'filename', 'filesize', 'checksum',
            'sample_accession', 'legacy_sample_id', 'disease_abbr',
            'tss_id', 'participant_id', 'sample_id', 'analyte_code',
            'sample_type', 'library_strategy', 'platform',
            'refassem_short_name']

class RequestDetailJSON(RequestDetail):
    """
    URI: analysisDetail uri.
    Fields: analysis_id, refassem_short_name,
        legacy_sample_id, center_name, checksum, disease_abbr,
        analyte_code, filename, filesize, library_strategy,
        last_modified, platform, sample_accession, sample_type,
        state, study, upload_date

    Used json response from wsapi/solr.
    """

    def patch_input_data(self):
        super(RequestDetailJSON, self).patch_input_data()
        self.format = self.FORMAT_JSON

    def patch_result(self, result, result_xml):
        try:
            if result.get('files'):
                for f in result['files']:
                    f['checksum'] = f['checksum']['#text']
            elif isinstance(result['filename'], list):
                result['files'] = []
                for i in range(len(result['filename'])):
                    result['files'].append({
                        'filename': result['filename'][i],
                        'checksum': result['checksum'][i],
                        'filesize': result['filesize'][i],
                    })
            result['filename'] = result['files'][0]['filename']
            result['checksum'] = result['files'][0]['checksum']
            result['files_size'] = result['files'][0]['filesize']
        except KeyError:
            result['filename'] = ''
            result['checksum'] = ''
            result['files_size'] = 0
        return result


class RequestFull(RequestBase):
    """
    URI: analysisFull uri.
    Fields: all.
    Raw xml added to results.
    """

    def patch_input_data(self):
        super(RequestFull, self).patch_input_data()
        self.uri = getattr(self, 'CGHUB_ANALYSIS_FULL_URI', self.uri)
        self.fields = None

    def patch_result(self, result, result_xml):
        if settings.API_TYPE == 'WSAPI':
            xml = result_xml
        elif settings.API_TYPE == 'SOLR':
            # create the same xml as WSAPI returns
            xml = build_wsapi_xml(result)
        new_result = super(RequestFull, self).patch_result(result, result_xml)
        new_result['reason'] = result['reason'].text or ''
        new_result['xml'] = xml
        return new_result


class ResultFromSOLRFile(SOLRRequest):
    """
    Used by RequestsTestCase.test_build_wsapi_xml
    """

    def get_source_file(self, url):
        filename = self.query['filename']
        return codecs.open(filename, 'r')


def get_results_for_ids(ids, sort_by=None):
    """
    Obtain all necessary attributes for specified analysis_ids
    """
    if not ids:
        return []
    api_request = RequestDetailJSON(query={'analysis_id': ids}, sort_by=sort_by)
    results = []
    for result in api_request.call():
        results.append(result)
    return results


class SearchByIDs(object):
    """
    Allows to search by multiple ids.
    """

    ID_ATTRS = ('analysis_id', 'aliquot_id', 'participant_id', 'sample_id')

    def __init__(self, ids, request_cls=RequestID, filters=None):
        """
        :param ids: list of ids to search by
        :param request_cls: Request class will be used to obtain results (RequestID, RequestDetail, ...)
        :param filters: filters dict to use in query
        """
        self.request_cls = request_cls
        self.filters = filters or {}
        self.legacy_sample_ids = []
        self.other_ids = []
        id_regexp = re.compile(settings.ID_PATTERN)
        for i in ids:
            if id_regexp.match(i.lower()):
                # other ids: aliquot_id, analysis_id, participant_id, sample_id
                self.other_ids.append(i.lower())
            else:
                self.legacy_sample_ids.append(i.upper())
        self.search()

    def search(self):
        self.results = {}
        if self.other_ids:
            for attr in self.ID_ATTRS:
                self.results[attr] = []
                query = dict(self.filters)
                query[attr] = self.other_ids
                api_request = self.request_cls(query=query)
                found = False
                for result in api_request.call():
                    self.results[attr].append(result)
                    found = True
                # stop if single id was found
                if found and len(self.other_ids) == 1:
                    break

        if self.legacy_sample_ids:
            self.results['legacy_sample_id'] = []
            query = dict(self.filters)
            query['legacy_sample_id'] = self.legacy_sample_ids
            api_request = self.request_cls(query=query)
            for result in api_request.call():
                self.results['legacy_sample_id'].append(result)

    def get_ids(self):
        ids = []
        for attr in self.results:
            for result in self.results[attr]:
                if result['analysis_id'] not in ids:
                    ids.append(result['analysis_id'])
        return ids

    def get_results(self):
        results = []
        ids = []
        for attr in self.results:
            for result in self.results[attr]:
                if result['analysis_id'] not in ids:
                    ids.append(result['analysis_id'])
                    results.append(result)
        return results

    def is_empty(self):
        return not any([val for key, val in self.results.iteritems()])
