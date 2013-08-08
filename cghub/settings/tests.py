import os.path

from apps import INSTALLED_APPS


DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# skip migrations while testing
SOUTH_TESTS_MIGRATE = True

TEST_CACHE_DIR = os.path.join(os.path.dirname(__file__), '../test_cache')
