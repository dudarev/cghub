from utils import proj


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': proj('db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

SITE_ID = 1

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_TZ = True

USE_I18N = True
USE_L10N = True

SECRET_KEY = 'f3=dg%b600m5aivknk-tld04ucg0a1yj&amp;4+1nxj#a!p3m6kkbp'

ROOT_URLCONF = 'cghub.urls'

WSGI_APPLICATION = 'cghub.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
