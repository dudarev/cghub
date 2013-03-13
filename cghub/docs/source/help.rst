Help
=================

Help hints for table and filters bar
----------------------------

Text for help hints for every table column, for table cells values and for filters can be specified in project settings.

``settings/help.py``:

.. code-block:: python

    # help.py

    COLUMN_HELP_HINTS = {
        'UUID': 'Help hint for UUID, and this is <a href="http://some/url/">link</a>, click to view help page!',
        'State': 'Some help text',
        'State:Live': 'Some help hint for Live State'
        ...

COLUMN_HELP_HINTS keys for table cells calculates as <column name>:<cell value>.

Help hints for cells for columns: 'UUID', 'Upload time', 'Last modified', 'Barcode' and 'File Size' are disabled.

In case, when help hint for specified key was not found, a new record will be added to log file, for example:

::

    INFO 2013-03-11 16:32:25,441 views 12187 47019968759552 Assembly key is missing
    INFO 2013-03-11 16:32:28,110 views 12187 47019968759552 Center key is missing
    INFO 2013-03-11 16:32:30,200 views 12187 47019968759552 Center:UNC-LCCC key is missing

Logging can be configured in :file:`cghub/setting/logging_settings.py`. SysLog handler used by default.

settings/logging_settings.py:

.. code-block:: python

    'help.hints': {
        'handlers': ['syslog'],
        'level': 'INFO',
        'propagate': True,
    },


Popups with help text
---------------------

To add new popup:
    - add new 'Help text' record in /admin/help/helptext/
    - add link with class="js-help-link" and with data-slug attribute equal to slug value specified in admin site before

For example:

.. code-block:: html

    <a href class="js-help-link" data-slug="uuid-help">Click to show UUID help</a>

When user click on this link, popup will be shown.

You can use such links in help hints:

.. code-block:: python

    COLUMN_HELP_HINTS = {
        'UUID': 'File identifier, <a href class="js-help-link" data-slug="uuid-help">click to view more detailed information</a>.',
        ...
