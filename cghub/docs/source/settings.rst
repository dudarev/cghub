Settings
=================


WSAPI
----------

It is possible to set some settings for wsapi app.

``settings/wsapi.py``:

.. code-block:: python

    WSAPI_CGHUB_SERVER = 'https://stage.cghub.ucsc.edu/'
    WSAPI_CGHUB_ANALYSIS_ID_URI = '/cghub/metadata/analysisId'
    WSAPI_CGHUB_ANALYSIS_DETAIL_URI = '/cghub/metadata/analysisDetail'
    WSAPI_CGHUB_ANALYSIS_FULL_URI = '/cghub/metadata/analysisFull'
    WSAPI_HTTP_ERROR_ATTEMPTS = 5
    WSAPI_HTTP_ERROR_SLEEP_AFTER = 1
    WSAPI_TESTING_CACHE_DIR = os.path.join(os.path.dirname(__file__), '../test_cache')

Use TESTING_MODE wsapi setting to enable caching results while testing.


Variables
----------

Some of cghub browser site settings specified in cghub/settings/variables.py file.
Most useful:

.. code-block:: python

    # if user will try to add to cart more than specified number of files,
    # confirmation popup will be shown
    MANY_FILES = 100

    # shows after ... Please contact admin:
    SUPPORT_EMAIL = 'support@cghub.ucsc.edu'

    # time, after which tooltip will be shown, in ms
    TOOLTIP_HOVER_TIME = 250


Celery
----------

To run periodic tasks (for now only related to :ref:`caching <caching>`) we use Celery.
Its settings are in ``settings/celery_settings.py``.

In ``local.py`` define BROKER_URL

:file:`local.py`:

.. code-block:: python

	# $ rabbitmqctl add_user myuser mypassword
	# $ rabbitmqctl add_vhost myvhost
	# $ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
	# Example
	# BROKER_URL = "amqp://cghub:cghub@localhost:5672/cghub"

	# BROKER_URL = "amqp://user:password@host:port/vhost"

:file:`celery_settings.py`:

.. code-block:: python

	import sys
	import djcelery

	from .cache import TIME_CHECK_CART_CACHE_INTERVAL, TIME_CHECK_API_CACHE_INTERVAL

	djcelery.setup_loader()

	CELERY_IMPORTS = (
	    "cghub.apps.cart.tasks",
	    )

	CELERYBEAT_SCHEDULE = {
	    #"clear-cart-cache": {
	    #    "task": "cghub.apps.cart.tasks.cache_clear_task",
	    #    "schedule": TIME_CHECK_CART_CACHE_INTERVAL,
	    #    },
	    }

	CELERY_RESULT_BACKEND = "amqp"
	CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

	if 'test' in sys.argv:
	    BROKER_URL = "django://"

	CELERYD_CONCURRENCY = 1

Celery configured to send logs to syslog by default. See :ref:`logging section <logging>`.

.. _caching:

Caching
---------

When items are added to the cart, XML for each result saves to cart cache.

Path to cart cache specified in settings:

.. code-block:: python

    # cache.py

    CART_CACHE_DIR = '/tmp/cart/'


Paging
-------------

Search results are paged when requested from the server. Paging is done by WSI API.
Default number of results per page may be set in ``settings/ui.py``:

.. code-block:: python

    # ui.py

    DEFAULT_PAGINATOR_LIMIT = 10

Columns ordering and styles
---------------------------

Columns ordering, styles and default state for the results table can be specified in project settings.
Default configuration is located in ``settings/ui.py``:

.. code-block:: python

    # ui.py

    TABLE_COLUMNS = (
        'Study',
        'Disease',
        'Disease Name',
        'Sample Type',
        ...

    COLUMN_STYLES = {
        'Analysis Id': {
            'width': 220, 'align': 'left', 'default_state': 'visible',
        },
        'Assembly': {
            'width': 120, 'align': 'left', 'default_state': 'visible',
        },
        ...


If style for column will be not specified, will be used default styles:

.. code-block:: python

    {
        'width': 100,
        'align': 'left',
        'default_state': 'visible'
    }

Available align values: center, justify, left, right, inherit.

Available default_state values: 'visible', 'hidden'.

Details list ordering
---------------------
Details list ordering can be specified in project settings.
Default configuration is located in ``settings/ui.py``:

.. code-block:: python

    # ui.py

    DETAILS_FIELDS = (
    'Analysis Id',
    'Study',
    'Disease',
    ...

Change values displayed in table
--------------------------------

Some column values can has an absurd names. To map them to something a human would understand can be used VALUE_RESOLVERS variable.

``settings/ui.py``:

.. code-block:: python

    def study_resolver(val):
        if val.find('Other_Sequencing_Multiisolate') != -1:
            return 'CCLE'
        return val

    VALUE_RESOLVERS = {
        'Study': study_resolver,
    }


Default filters
---------------

Default filters can be specified in settings. For example:

.. code-block:: python

    # ui.py

    DEFAULT_FILTERS = {
        'study': ('phs000178', '*Other_Sequencing_Multiisolate'),
        'state': ('live',),
        'upload_date': '[NOW-7DAY TO NOW]',
    }

Filters can be found in :file:`cghub/apps/core/filters_storage_full.py` or copied from browser's address field, for example, for specified DEFAULT_FILTERS, address will be next:

::

    https://cghub.ucsc.edu/browser/search/?upload_date=[NOW-7DAY+TO+NOW]&study=(phs000178+OR+*Other_Sequencing_Multiisolate)&state=(live)

.. _logging:

Logging
--------------

:file:`cghub/setting/local.py.default` contains the example of a SysLogHadler usage. Default configuration located in :file:`cghub/setting/logging_settings.py`.

.. code-block:: python

    from logging.handlers import SysLogHandler

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
            'wsapi.request': {
                # use to disable this logger
                # 'handlers': ['null'],
                'handlers': ['syslog'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'cart': {
                'handlers': ['syslog'],
                'level': 'ERROR',
                'propagate': True,
            }
        },
    }

Usage example:

.. code-block:: bash

	>>> import logging
	>>> l = logging.getLogger('django.request')
	>>> l.error('Error msg')
	................
	jey@travelmate:/var/log$ tail -1 syslog
	Nov 14 10:22:13 travelmate ERROR 2012-11-14 02:22:13,599 <console> 17654 1077970624 Error msg

For more information see the `complete SysLogHandler reference`_ .

.. _`complete SysLogHandler reference`: http://docs.python.org/2/library/logging.handlers.html#sysloghandler

Celery configured to send logs to syslog with address == SYSLOG_ADDRESS, see ``cghub/apps/core/__init__.py``.
