import os.path
import sys

from lxml import objectify

from django.conf import settings

from wsapi.api import Results
from wsapi.api import request as api_request

from cghub.apps.core.utils import get_wsapi_settings


WSAPI_SETTINGS = get_wsapi_settings()

# use wsapi cache when testing
USE_WSAPI_CACHE = 'test' in sys.argv


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
        return self.message or ('File for analysis_id={0}, which was last modified {1} '
            'not exists, may be it was updated'.format(
                                self.analysis_id,
                                self.last_modified)) 


def get_cart_cache_file_path(analysis_id, last_modified, short=False):
    """
    Calculate path to cache file

    :param analysis_id: file analysis_id
    :param last_modified: file last_modified
    :short: if True - will be returned path to file contains cutted amount of attributes
    """
    return os.path.join(
            settings.CART_CACHE_DIR,
            analysis_id,
            last_modified,
            'analysis{0}.xml'.format('Short' if short else 'Full'))


def save_to_cart_cache(analysis_id, last_modified):
    """
    Save file to {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisFull.xml
    and cutted version saves to
    {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisShort.xml
    Raise AnalysisFileException if file does not exist or was updated

    returns wsapi.api.Results object if success
    """
    # to protect files outside cache dir
    if analysis_id.find('..') != -1 or last_modified.find('..') != -1:
        raise AnalysisFileException(analysis_id, last_modified,
                                message='Bad analysis_id or last_modified')
    path = settings.CART_CACHE_DIR
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path, analysis_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path, last_modified)
    if not os.path.isdir(path):
        os.makedirs(path)
    path_full = os.path.join(path, 'analysisFull.xml')
    path_short = os.path.join(path, 'analysisShort.xml')
    if not (os.path.exists(path_full) and os.path.exists(path_short)):
        result = api_request(
                query='analysis_id={0}'.format(analysis_id),
                ignore_cache=not USE_WSAPI_CACHE,
                use_api_light=False,
                settings=WSAPI_SETTINGS)
        if not hasattr(result, 'Result') or int(result.Hits.text) != 1:
            raise AnalysisFileException(analysis_id, last_modified)
        if result.Result.last_modified != last_modified:
            raise AnalysisFileException(analysis_id, last_modified)
        with open(path_full, 'w') as f:
            f.write(result.tostring())
        with open(path_short, 'w') as f:
            result.remove_attributes()
            f.write(result.tostring())
        return result
    return Results.from_file(path_full, settings=WSAPI_SETTINGS)


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
    # if file not exists or was updated - AnalysisFileException exception will be raised
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
    if os.path.exists(path):
        return Results.from_file(path, settings=WSAPI_SETTINGS)
    # if file not exists or was updated - AnalysisFileException exception will be raised
    return save_to_cart_cache(analysis_id, last_modified)


def join_analysises(data, short=False, live_only=False):
    """
    Join xml files with specified ids.
    If file exists in cache, it will be used, otherwise, file will be downloaded and cached.

    :param data: ((analysis_id, last_modified), (analysis_id, last_modified), ...)
    :param short: if True - file will be contains only most necessary attributes
    :param live_only: if True - files with state attribute != 'live' will be not included to results
    """
    results = None
    results_counter = 1
    for analysis_id, last_modified in data:
        try:
            result = get_analysis(analysis_id, last_modified, short=False)
            if live_only and result.Result.state != 'live':
                continue
        except AnalysisFileException:
            continue
        if results is None:
            results = result
            results.Query.clear()
            results.Hits.clear()
        else:
            result.Result.set('id', u'{0}'.format(results_counter))
            # '+ 1' because the first two elements (0th and 1st) are Query and Hits
            results.insert(results_counter + 1, result.Result)
        results_counter += 1
    return results
