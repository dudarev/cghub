import os.path
import sys

from django.conf import settings

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
    def __init__(self, analysis_id, last_modified):
        self.analysis_id = analysis_id
        self.last_modified = last_modified

    def __str__(self):
        return ('File for analysis_id={0}, which was last modified {1} '
            'not exists, may be it was updated'.format(
                                self.analysis_id,
                                self.last_modified)) 


def save_to_cache(analysis_id, last_modified):
    """
    Save file to {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisFull.xml
    and cutted version saves to
    {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisShort.xml
    Raise AnalysisFileException if file does not exist or was updated
    """
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


def get_analysis_file(analysis_id, modification_time):
    path = os.path.join(settings.CART_CACHE_DIR, analysis_id, modification_time)
    path_full = os.path.join(path, 'analysisFull.xml')
    path_short = os.path.join(path, 'analysisShort.xml')
    if os.path.exists(path_full) and os.path.exists(path_short):
        return (path_full, path_short)
    # if file not exists or was updated - AnalysisFileException exception will be raised
    save_to_cache(analysis_id, modification_time)
    return (path_full, path_short)
    
