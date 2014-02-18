Settings
=================


API
---

It is possible to set some settings for cghub_python_api.

``settings/api.py``:

.. code-block:: python

    CGHUB_SERVER = 'https://192.35.223.223'
    CGHUB_SERVER_SOLR_URI = '/solr/select/'
    API_HTTP_ERROR_ATTEMPTS = 5
    API_HTTP_ERROR_SLEEP_AFTER = 1
    API_TYPE = 'WSAPI'

Can be used SOLR or WSAPI. To switch between them, only need to specify API_TYPE and CGHUB_SERVER.

Variables
---------

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

Caching
-------

When items are added to the cart, XML for each result saves to cart cache.

Path to cart cache specified in settings:

.. code-block:: python

    # cache.py

    FULL_METADATA_CACHE_DIR = '/tmp/full_metadata_cache/'


Paging
------

Search results are paged when requested from the server. Paging is done by WSI API.
List of allowed numbers of items per page may be set in ``settings/variables.py``:

.. code-block:: python

    # settings/variables.py

    PAGINATOR_LIMITS = [15, 25, 50]

Default items per page is PAGINATOR_LIMITS[0].


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

Table row menu custom fields
----------------------------

Can be configured in project settings.
Default configuration is located in ``settings/ui.py``:

Allows to add custom table row menu items.
Every custom menu item should consist from menu item name and link
(every custom menu item is just a link).
Details menu item (open item details popup) adds by default.

Format:
list <Menu item name>, <function that returns link>

Example:

::

    def details_page_menu_item(values):
        return reverse('item_details', args=(values.get('analysis_id'),))

    ROW_MENU_ITEMS = [
        ('Show details in new window', details_page_menu_item),
        ...
    ]

values - row data dict.
Menu item will be shown only if link is not None.

Change values displayed in table
--------------------------------

Some column values can has an absurd names. To map them to something a human would understand can be used VALUE_RESOLVERS variable.

``settings/ui.py``:

Format:
dict <Column name>:<function>

function receives value should be displayed and api result
(api result is a dict, example: {'state': 'live', 'study': 'CCLE', ...})
and should return new value, for example:

.. code-block:: python

    def study_resolver(value, result):
        if value.find('Other_Sequencing_Multiisolate') != -1:
            return 'CCLE'
        return value

    def some_field_resolver(value, result):
        if result['state'] == 'live':
            return value
        return ''

    VALUE_RESOLVERS = {
        'Study': study_resolver,
        'Some Field': some_field_resolver,
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

Filters can be found in :file:`cghub/settings/filters.py` or copied from browser's address field, for example, for specified DEFAULT_FILTERS, address will be next:

::

    https://cghub.ucsc.edu/browser/search/?upload_date=[NOW-7DAY+TO+NOW]&study=(phs000178+OR+*Other_Sequencing_Multiisolate)&state=(live)

.. _logging:

Logging
-------

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
