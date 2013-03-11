import sys
from logging.handlers import SysLogHandler
from utils import proj

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
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
            # uncomment to save logs to /dev/log/syslog
            # 'address': '/dev/log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
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
