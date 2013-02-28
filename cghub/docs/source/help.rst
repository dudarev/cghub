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

    Disease:BLCA key is missing
    Disease Name:Lung adenocarcinoma key is missing

This log file located in logs folder by default.

settings/logging_settings.py:

.. code-block:: python

    HELP_LOGGING_FILE = proj('logs/help.log')


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
