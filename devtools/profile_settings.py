import os.path

from cghub.settings import *


FULL_METADATA_CACHE_DIR = os.path.join(
        os.path.dirname(__file__),
        'full_metadata_cache/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(
                        os.path.dirname(__file__),
                        'profile_db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
