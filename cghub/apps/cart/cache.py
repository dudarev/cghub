import os.path
import sys

from lxml import objectify

from django.conf import settings

from cghub.wsapi.api import Results
from cghub.wsapi.api import request as api_request
from cghub.wsapi.utils import makedirs_group_write, generate_tmp_file_name

from cghub.apps.core.utils import get_wsapi_settings


WSAPI_SETTINGS = get_wsapi_settings()

# use wsapi cache when testing
USE_WSAPI_CACHE = 'test' in sys.argv

RESULT_START = '<Result id="1">'
RESULT_STOP = '</Result>'
FSIZE_START = '<filesize>'
FSIZE_STOP = '</filesize>'


class AnalysisFileException(Exception):
    """
    Exception raises when file with specified analysis_id does not exists
    or was updated
    """
    def __init__(self, analysis_id, last_modified, message=''):
        self.analysis_id = analysis_id
        self.last_modified = last_modified
        self.message = message

    def __str__(self):
        return 'File for analysis_id={0}, which was last modified {1}. {2}'.format(
                                self.analysis_id,
                                self.last_modified,
                                self.message) 


def get_cart_cache_file_path(analysis_id, last_modified, short=False):
    """
    Calculate path to cache file

    c9d9d785-9fb0-11e2-99fa-001b218b57f8/...
    would become:
    c9/d9/c9d9d785-9fb0-11e2-99fa-001b218b57f8/...

    :param analysis_id: file analysis_id
    :param last_modified: file last_modified
    :short: if True - will be returned path to file contains cutted amount of attributes
    """
    return os.path.join(
            settings.CART_CACHE_DIR,
            analysis_id[:2],
            analysis_id[2:4],
            analysis_id,
            last_modified,
            'analysis{0}.xml'.format('Short' if short else 'Full'))


def is_cart_cache_exists(analysis_id, last_modified):
    return (os.path.exists(get_cart_cache_file_path(analysis_id, last_modified)) and
        os.path.exists(get_cart_cache_file_path(analysis_id, last_modified, short=True)))


def save_to_cart_cache(analysis_id, last_modified):
    """
    Save file to {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisFull.xml
    and cutted version saves to
    {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisShort.xml
    Raise AnalysisFileException if file with specified analysis_id does not exist.
    If file was updated - use most recent version.

    c9d9d785-9fb0-11e2-99fa-001b218b57f8/...
    would become:
    c9/d9/c9d9d785-9fb0-11e2-99fa-001b218b57f8/...

    """
    # to protect files outside cache dir
    if (not analysis_id or
        not last_modified or
        analysis_id.find('..') != -1 or
        last_modified.find('..') != -1):
        raise AnalysisFileException(
                analysis_id, last_modified,
                message='Bad analysis_id or last_modified')
    if is_cart_cache_exists(analysis_id, last_modified):
        return
    path = settings.CART_CACHE_DIR
    if not os.path.isdir(path):
        makedirs_group_write(path)
    folders = (
                analysis_id[:2],
                analysis_id[2:4],
                analysis_id,
                last_modified)
    for folder in folders:
        path = os.path.join(path, folder)
        if not os.path.isdir(path):
            makedirs_group_write(path)
    path_full = os.path.join(path, 'analysisFull.xml')
    path_short = os.path.join(path, 'analysisShort.xml')
    if not (os.path.exists(path_full) and os.path.exists(path_short)):
        result = api_request(
                query='analysis_id={0}'.format(analysis_id),
                ignore_cache=not USE_WSAPI_CACHE,
                full=True,
                use_api_light=False,
                settings=WSAPI_SETTINGS)
        if not hasattr(result, 'Result') or int(result.Hits.text) != 1:
            raise AnalysisFileException(
                    analysis_id, last_modified,
                    message='File with specified analysis_id not found')
        # if result.Result.last_modified != last_modified:
        # load most recent version
        # example tmp file name: 14985-MainThread-my-pc.tmp
        path_tmp = os.path.join(path, generate_tmp_file_name())
        with open(path_tmp, 'w') as f:
            f.write(result.tostring())
            f.close()
        # manage in a atomic manner
        os.rename(path_tmp, path_full)
        with open(path_tmp, 'w') as f:
            result.remove_attributes()
            f.write(result.tostring())
            f.close()
        os.rename(path_tmp, path_short)


def get_analysis_path(analysis_id, last_modified, short=False):
    """
    returns path to analysis file on disk

    :param analysis_id: file analysis_id
    :param last_modified: file last_modified
    :param short: if True - will be returned path to file contains cutted amount of attributes
    """
    path = get_cart_cache_file_path(analysis_id, last_modified, short=short)
    if os.path.exists(path):
        return path
    save_to_cart_cache(analysis_id, last_modified)
    return path


def get_analysis(analysis_id, last_modified, short=False):
    """
    returns wsapi.api.Results object

    :param analysis_id: file analysis_id
    :param last_modified: file last_modified
    :param short: if True - will be returned path to file contains cutted amount of attributes
    """
    path = get_cart_cache_file_path(analysis_id, last_modified, short=short)
    if not os.path.exists(path):
        save_to_cart_cache(analysis_id, last_modified)
    result = Results.from_file(path, settings=WSAPI_SETTINGS)
    return result


def get_analysis_xml(analysis_id, last_modified, short=False):
    """
    Returns part of xml file (Result content) stored in cache, and files size

    :param analysis_id: file analysis_id
    :param last_modified: file last_modified
    :param short: if True - will be returned path to file contains cutted amount of attributes

    Returns:
    (xml, files_size)
    """
    path = get_cart_cache_file_path(analysis_id, last_modified, short=short)
    if not os.path.exists(path):
        # if file not exists - most recent file will be downloaded
        save_to_cart_cache(analysis_id, last_modified)
    with open(path, 'r') as f:
        result = f.read()
    start = result.find(RESULT_START) + len(RESULT_START)
    stop = result.find(RESULT_STOP)
    result = result[start:stop]
    # find files size
    files_size = 0
    start = result.find(FSIZE_START)
    while start != -1:
        stop = result.find(FSIZE_STOP, start + 1)
        files_size += int(result[start+len(FSIZE_START):stop])
        start = result.find(FSIZE_START, start + 1)
    return result, files_size
