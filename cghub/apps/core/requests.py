import sys
import urllib2
import hashlib
import os
import logging

from cghub_python_api import WSAPIRequest, SOLRRequest
from cghub_python_api.utils import urlopen

from django.conf import settings

from .attributes import ATTRIBUTES


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
        os.makedirs(CACHE_DIR)
    md5 = hashlib.md5(url)
    path = os.path.join(CACHE_DIR, '%s_%s.%s.cache' % (
            settings.API_TYPE.lower(), md5.hexdigest(), format))
    if os.path.exists(path):
        return open(path, 'r')
    headers = {'Accept': FORMAT_CHOICES.get(format, FORMAT_CHOICES['xml'])}
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read()
    with open(path, 'w') as f:
        f.write(content)
    return open(path, 'r')


class RequestBase(REQUEST_CLASS):

    def patch_input_data(self):
        server_url = getattr(settings, 'CGHUB_SERVER')
        if server_url:
            self.server_url = server_url

    def get_xml_file(self, url):
        if 'test' in sys.argv:
            return get_from_test_cache(url=url)
        api_logger.error(urllib2.unquote(url))
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
        new_result = super(RequestFull, self).patch_result(result, result_xml)
        new_result['xml'] = (
                result_xml.replace('\t', '').replace('\n', ''))
        return new_result


class ResultFromFile(RequestFull):
    """
    Allows to create cghub_python_apy.api.Request
    from analysis xml stored in local file
    """

    def get_xml_file(self, url):
        filename = self.query['filename']
        return open(filename, 'r')
