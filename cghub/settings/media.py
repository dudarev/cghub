import os
from datetime import timedelta

from cghub.settings.utils import root

MEDIA_ROOT = root('media')
API_RESULTS_CACHE_FOLDER = os.path.join(MEDIA_ROOT, 'api_results_cache')
MEDIA_URL = ''

TIME_DELETE_CACHE_FILES_OLDER = timedelta(hours=24)
TIME_CHECK_CACHE_INTERVAL = timedelta(hours=12)
