import codecs
import os.path

from urllib2 import URLError
from lxml import etree

from django.conf import settings

from cghub.apps.core.utils import (
        makedirs_group_write, generate_tmp_file_name)
from cghub.apps.core.requests import RequestFull


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
    parser = etree.XMLParser(
            remove_blank_text=True, ns_clean=True,
            recover=True)
    tree = etree.fromstring(result['xml'], parser)
    tree = tree.xpath('//Result[1]/child::*')
    xml = ''
    space = '    '
    for el in tree:
        xml += etree.tostring(el, pretty_print=True)
    xml = ('\n%s' % space).join(xml.split('\n'))
    with codecs.open(tmp_path, 'w', encoding='utf-8') as f:
        f.write('%s%s' % (space, xml.strip()))
        f.close()
    # manage in a atomic manner
    os.rename(tmp_path, file_path)


def get_analysis_xml(analysis_id, last_modified):
    """
    Returns part of xml file (Result content) stored in cache
    """
    path = get_cart_cache_file_path(analysis_id, last_modified)
    if not os.path.exists(path):
        # if file not exists - most recent file will be downloaded
        save_to_cart_cache(analysis_id, last_modified)
    with codecs.open(path, 'r', encoding='utf-8') as f:
        result = f.read()
    start = result.find('<filesize>')
    files_size = 0
    # get only first file size
    if start != -1:
        stop = result.find('</filesize>', start + 1)
        files_size = int(result[start + len('<filesize>'):stop])
    return result, files_size
