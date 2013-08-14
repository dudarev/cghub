import os
from datetime import timedelta

from cghub.settings.utils import root

MEDIA_ROOT = root('media')
FULL_METADATA_CACHE_DIR = '/tmp/full_metadata_cache/'
MEDIA_URL = ''

TIME_DELETE_CART_CACHE_FILES_OLDER = timedelta(hours=2)
TIME_CHECK_CART_CACHE_INTERVAL = timedelta(hours=1)

TIME_DELETE_API_CACHE_FILES_OLDER = timedelta(hours=2)
TIME_CHECK_API_CACHE_INTERVAL = timedelta(hours=1)
