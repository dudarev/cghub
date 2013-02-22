import os
from datetime import timedelta

from cghub.settings.utils import root

MEDIA_ROOT = root('media')
CART_CACHE_DIR = '/tmp/wsapi/'
MEDIA_URL = ''

TIME_DELETE_CART_CACHE_FILES_OLDER = timedelta(hours=2)
TIME_CHECK_CART_CACHE_INTERVAL = timedelta(hours=1)
