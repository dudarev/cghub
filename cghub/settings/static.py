from utils import root


STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    root('static'),
    )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
