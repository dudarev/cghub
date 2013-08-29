import sys
import urllib2
import hashlib
import os
import logging
import datetime
import codecs

from cghub_python_api import WSAPIRequest, SOLRRequest
from cghub_python_api.utils import urlopen

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .attributes import (
        ATTRIBUTES, SORT_BY_ATTRIBUTES, ADDITIONAL_ATTRIBUTES)
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
        return codecs.open(path, 'r', encoding='utf-8')
    headers = {'Accept': FORMAT_CHOICES.get(format, FORMAT_CHOICES['xml'])}
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read()
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
            'server_url': settings.CGHUB_SERVER})
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

    def get_xml_file(self, url):
        if 'test' in sys.argv:
            return get_from_test_cache(url=url)
        api_logger.debug(urllib2.unquote(url))
        return urlopen(
                url=url,
                max_attempts=getattr(settings, 'API_HTTP_ERROR_ATTEMPTS', 5),
                sleep_time=getattr(settings, 'API_HTTP_ERROR_SLEEP_AFTER', 1))

    def patch_result(self, result, result_xml):
        new_result = {}
        for attr in ATTRIBUTES:
            if result[attr].exist:
                new_result[attr] = result[attr].text
        new_result['filename'] = result['filename.0'].text
        try:
            new_result['files_size'] = int(result['filesize.0'].text)
        except TypeError:
            new_result['files_size'] = 0
        new_result['checksum'] = result['checksum.0'].text
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
    Fields: analysis_id, last_modified, state, filesize.
    """

    def patch_input_data(self):
        super(RequestMinimal, self).patch_input_data()
        self.uri = getattr(self, 'CGHUB_ANALYSIS_DETAIL_URI', self.uri)
        self.fields = ['analysis_id', 'last_modified', 'state', 'filesize']

    def patch_result(self, result, result_xml):
        return {
                'analysis_id': result['analysis_id'].text,
                'last_modified': result['last_modified'].text,
                'state': result['state'].text,
                'files_size': result['filesize.0'].text}


class RequestDetail(RequestBase):
    """
    URI: analysisDetail uri.
    Fields: analysis_id, refassem_short_name,
        legacy_sample_id, center_name, checksum, disease_abbr,
        analyte_code, filename, filesize, library_strategy,
        last_modified, platform, sample_accession, sample_type,
        state, study, upload_date
    """

    def patch_input_data(self):
        super(RequestDetail, self).patch_input_data()
        self.uri = getattr(self, 'CGHUB_ANALYSIS_DETAIL_URI', self.uri)
        self.fields = [
            'analysis_id', 'refassem_short_name',
            'legacy_sample_id', 'center_name', 'checksum', 'disease_abbr',
            'analyte_code', 'filename', 'filesize', 'library_strategy',
            'last_modified', 'platform', 'sample_accession', 'sample_type',
            'state', 'study', 'upload_date']


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
        # additional attributes
        for attr in ADDITIONAL_ATTRIBUTES:
            if result[attr].exist:
                new_result[attr] = result[attr].text
        if settings.API_TYPE == 'WSAPI':
            new_result['xml'] = xml.decode('utf-8')
        else:
            new_result['xml'] = xml
        return new_result


class ResultFromWSAPIFile(WSAPIRequest):
    """
    Allows to create cghub_python_apy.api.Request
    from analysis xml stored in local file
    """

    def get_xml_file(self, url):
        filename = self.query['filename']
        return codecs.open(filename, 'r')

    def patch_result(self, result, result_xml):
        new_result = {}
        for attr in ATTRIBUTES:
            if result[attr].exist:
                new_result[attr] = result[attr].text
        # additional attributes
        for attr in ADDITIONAL_ATTRIBUTES:
            if result[attr].exist:
                new_result[attr] = result[attr].text
        new_result['filename'] = result['filename.0'].text
        try:
            new_result['files_size'] = int(result['filesize.0'].text)
        except TypeError:
            new_result['files_size'] = 0
        new_result['checksum'] = result['checksum.0'].text
        if settings.API_TYPE == 'WSAPI':
            new_result['xml'] = result_xml.decode('utf-8')
        else:
            new_result['xml'] = result_xml
        return new_result


class ResultFromSOLRFile(SOLRRequest):
    """
    Used by RequestsTestCase.test_build_wsapi_xml
    """

    def get_xml_file(self, url):
        filename = self.query['filename']
        return codecs.open(filename, 'r')


def get_results_for_ids(ids):
    """
    Obtain all necessary attributes for specified analysis_ids
    """
    if not ids:
        return []
    api_request = RequestDetail(query={'analysis_id': ids})
    results = []
    for result in api_request.call():
        results.append(result)
    return results
