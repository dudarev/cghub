import os.path
import codecs

from urllib2 import URLError

from django.conf import settings

from cghub.apps.core.utils import (
                        makedirs_group_write, generate_tmp_file_name,
                        xml_add_spaces)
from cghub.apps.core.requests import RequestFull, ResultFromWSAPIFile


RESULT_START = '<Result id="1">'
RESULT_STOP = '</Result>'
FSIZE_START = '<filesize>'
FSIZE_STOP = '</filesize>'


class AnalysisException(Exception):
    """
    Exception raises when file with specified analysis_id does not exists
    or was updated
    """
    def __init__(self, analysis_id, last_modified, message=''):
        self.analysis_id = analysis_id
        self.last_modified = last_modified
        self.message = message

    def __str__(self):
        return 'Analysis for analysis_id={0} that was last modified {1}. {2}'.format(
                self.analysis_id,
                self.last_modified,
                self.message)


def get_cart_cache_file_path(analysis_id, last_modified):
    """
    Calculate path to cache file

    c9d9d785-9fb0-11e2-99fa-001b218b57f8/...
    would become:
    c9/d9/c9d9d785-9fb0-11e2-99fa-001b218b57f8/...
    """
    return os.path.join(
            settings.FULL_METADATA_CACHE_DIR,
            analysis_id[:2],
            analysis_id[2:4],
            analysis_id,
            last_modified,
            'analysis.xml')


def is_cart_cache_exists(analysis_id, last_modified):
    """
    Returns path to cart cache file with specified analysis_id and last_modified
    """
    return os.path.exists(get_cart_cache_file_path(analysis_id, last_modified))


def save_to_cart_cache(analysis_id, last_modified):
    """
    Save file to {CACHE_ROOT}/{analysis_id}/{modification_time}/analysis.xml
    Raise AnalysisException if analysis with specified analysis_id does not exist.
    If file was updated - use most recent version.
    """
    # to protect files outside cache dir
    if (not analysis_id or
        not last_modified or
        analysis_id.find('..') != -1 or
        last_modified.find('..') != -1):
        raise AnalysisException(
                analysis_id, last_modified, message='Bad analysis_id or last_modified')
    if is_cart_cache_exists(analysis_id, last_modified):
        return
    dir_path = settings.FULL_METADATA_CACHE_DIR
    if not os.path.isdir(dir_path):
        makedirs_group_write(dir_path)
    folders = (
                analysis_id[:2],
                analysis_id[2:4],
                analysis_id,
                last_modified)
    for folder in folders:
        dir_path = os.path.join(dir_path, folder)
        if not os.path.isdir(dir_path):
            makedirs_group_write(dir_path)
    file_path = os.path.join(dir_path, 'analysis.xml')
    try:
        api_request = RequestFull(query={'analysis_id': analysis_id})
        result = api_request.call().next()
    except (URLError, StopIteration):
        raise AnalysisException(
                analysis_id,
                last_modified,
                message='Analysis with specified analysis_id does not exists')
    # if result['last_modified'] != last_modified:
    # load most recent version
    # example tmp file name: 14985-MainThread-my-pc.tmp
    tmp_path = os.path.join(dir_path, generate_tmp_file_name())
    xml = result['xml'].replace('\t', '').replace('\n', '')
    while xml.find('  ') != -1:
        xml = xml.replace('  ', ' ')
    xml = xml.replace('> <', '><')
    formatted_xml = u''
    for s in xml_add_spaces(xml, space=0, tab=2):
        formatted_xml += s
    with codecs.open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(formatted_xml.strip())
        f.close()
    # manage in a atomic manner
    os.rename(tmp_path, file_path)


def get_analysis_path(analysis_id, last_modified):
    """
    returns path to analysis file on disk
    """
    path = get_cart_cache_file_path(analysis_id, last_modified)
    if os.path.exists(path):
        return path
    save_to_cart_cache(analysis_id, last_modified)
    return path


def get_analysis(analysis_id, last_modified):
    """
    returns analysis dict
    """
    path = get_cart_cache_file_path(analysis_id, last_modified)
    if not os.path.exists(path):
        save_to_cart_cache(analysis_id, last_modified)
    api_request = ResultFromWSAPIFile(query={'filename': path})
    return api_request.call().next()


def get_analysis_xml(analysis_id, last_modified, short=False):
    """
    Returns part of xml file (Result content) stored in cache
    """
    path = get_cart_cache_file_path(analysis_id, last_modified)
    if not os.path.exists(path):
        # if file not exists - most recent file will be downloaded
        save_to_cart_cache(analysis_id, last_modified)
    with codecs.open(path, 'r', encoding='utf-8') as f:
        result = f.read()
    start = result.find(RESULT_START) + len(RESULT_START)
    stop = result.find(RESULT_STOP)
    result = result[start:stop]
    start = result.find(FSIZE_START)
    files_size = 0
    # get only first file size
    if start != -1:
        stop = result.find(FSIZE_STOP, start + 1)
        files_size = int(result[start + len(FSIZE_START):stop])
    if short:
        attributes_to_remove = (
                'analysis_xml', 'experiment_xml', 'run_xml',
                'sample_accession', 'legacy_sample_id',
                'disease_abbr', 'tss_id', 'participant_id', 'sample_id',
                'analyte_code', 'sample_type', 'library_strategy',
                'platform')
        for attribute in attributes_to_remove:
            start_str = '<%s>' % attribute
            stop_str = '</%s>' % attribute
            start = result.find(start_str)
            stop = result.find(stop_str, start)
            if start != -1 and stop != -1:
                stop += len(stop_str)
                # remove empty line
                while start != 0 and result[start - 1] != '>':
                    start -= 1
                result = u'%s%s' % (result[:start], result[stop:])
    return result, files_size
