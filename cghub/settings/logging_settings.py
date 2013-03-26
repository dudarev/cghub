import sys
from logging.handlers import SysLogHandler
from utils import proj


SYSLOG_ADDRESS = '/dev/log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'syslog': {
            'level':'INFO',
            'class':'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'facility': SysLogHandler.LOG_LOCAL2,
            'address': SYSLOG_ADDRESS,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['syslog'],
            'level': 'ERROR',
            'propagate': True,
        },
        'help.hints': {
            'handlers': ['syslog'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
