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

# according to http://docs.celeryproject.org/en/latest/django/unit-testing.html#testing-with-django:
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

TEST_CACHE_DIR = os.path.join(os.path.dirname(__file__), '../test_cache')
