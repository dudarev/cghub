INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    ]

INSTALLED_APPS += [
    'cghub.apps.core',
    'cghub.apps.cart',
    'cghub.apps.help',
    ]

INSTALLED_APPS += [
    'debug_toolbar',
    'south',
    'django_coverage',
    'djcelery',
    "kombu.transport.django",
    ]

