import os
from cghub.settings.utils import root

MEDIA_ROOT = root('media')
API_RESULTS_CACHE_FOLDER = os.path.join(MEDIA_ROOT, 'api_results_cache')
MEDIA_URL = ''
