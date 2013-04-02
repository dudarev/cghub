.. How it works

============
How it works
============

Help
====

Help hints
----------

Hints shows for table cells, filters and other elements marked by class. Time, after which tooltip will be shown, specified in ``cghub/static/js/help.js`` - see ``hoverTime`` variable.

.. code-block:: js

    cghub.help = {
        hoverTime: 1500, /* time, after which tooltip will be shown, in ms */

Text for help hints for every table column, for table cells values, for filters and othe elements can be specified in project settings.

``settings/help.py``:

.. code-block:: python

    # help.py

    HELP_HINTS = {
        'Analysis Id': 'Sample tooltip for "UUID", and this is <a href="#" class="js-help-link" data-slug="analysis-id">link</a>, click to view help page!',
        'Study': 'Sample tooltip for "Study"',
        'Study:TCGA': 'Sample tooltip for "Study/TCGA"',
        'Study:TCGA Benchmark': 'Sample tooltip for "Study/TCGA Benchmark"',
        # help hints for filter titles
        'filter:Study': 'Sample tooltip for filter "Study"',
        # common help hint, can be added for any element
        'common:some-div': 'Sample tooltip for div-element',
    }

HELP_HINTS keys for table cells calculates as <column name>:<cell value>.

In case of common help hint, key will start from 'common:'.
To add tooltip to, for example, some div element, we should add 'js-commont-tooltip' class to element and specify key it will be recognized by. Example:

::

    # HTML:
    <div class="someclass js-common-tooltip" data-tag="some-key">Some content</div>

    # help.py:
    HELP_HINTS = {
        'common:some-tag': 'Some hint' 

Help hints for cells for columns: 'Analysis Id', 'Uploaded', 'Last modified', 'Barcode' and 'File Size' are disabled.

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

    <a href class="js-help-link" data-slug="analysis_id-help">Click to show Analysis Id help</a>

When user click on this link, popup will be shown.

You can use such links in help hints:

.. code-block:: python

    COLUMN_HELP_HINTS = {
        'Analysis Id': 'File identifier, <a href class="js-help-link" data-slug="analysis_id-help">click to view more detailed information</a>.',
        ...

Celery tasks
============

A `task <http://docs.celeryproject.org/en/latest/userguide/tasks.html#tasks>`__ is a class that can be created out of any callable. It performs dual roles in that it defines both what happens when a task is called (sends a message), and what happens when a worker receives that message.

Task can be easily created from any callable by using ``task()`` decorator.

It is a common practice in Django to put tasks in their own module named tasks.py, and the worker will automatically go through the apps in INSTALLED_APPS to import these modules.

Tasks in this project stored in:
    - `cghub/apps/core/tasks.py`
    - `cghub/apps/cart/tasks.py`

There are next tasks:

.. autofunction:: cghub.apps.core.tasks.api_cache_clear_task

.. autofunction:: cghub.apps.cart.tasks.cache_results_task

.. autofunction:: cghub.apps.cart.tasks.add_files_to_cart_by_query

Caching
=======

There are next types of cache files:
    - api cache:
        - files obtained by api.py. Theirs names calculated as hash from query used to obtain them
        - files obtained by api.py using analysisId uri (when get_attributes==False), they ends with '-no-attr'
        - list of ids created by api_light.py, they have extension '.ids'
    - cart cache
        - cached files for one analysis id, used when collecting metadata, manifest of summary file. Adds when adding files to cart if not exists yet. Can be saved few versions of files for different last_modified. Path to these files calculated using next pattern: {CART_CACHE_DIR}/{analysis_id}/{last_modified}/analysis[Full|Short].xml

Folders where cache should be stored specified in settings (CART_CACHE_DIR).

Cart cache
----------

When user adds some files to cart, this files will be saved to cache if they not exists here yet (using cache_results_task).
For every added file will be created two files in cache: one is analysisFull.xml and second is analysisShort.xml that contains only most necessary attributes and used to build manifest file.

Path to analysis file can be obtained by next function:

.. autofunction:: cghub.apps.cart.cache.get_analysis_path

To get wsapi.api.Result object for specified analysis_id and last_modified can be used next function:

.. autofunction:: cghub.apps.cart.cache.get_analysis

If file will be not  cached, program will try to upload it. In case when file with specified analysis_id for specified last_modified will be not found, will be raised AnalysisFileException exception.

Adding files to cart
====================

There are two ways to add items to cart:
    - select few items and add them to cart
    - add all items obtained by specified query

Adding selected files to cart
-----------------------------

The following sequence of actions are performing:
    - when user click on 'Add to cart', attributes values for selected files that stored in table transmitted
    - obtained attributes are saved to cart (stored in Session)
    - if file not in cache yet, will be created task to cache it

Adding all files to cart
------------------------

Here are next sequence of actions:
    - when user click 'Add all to cart', transmitted only current query
    - then will be created task to obtain all attributes for specified query and fill cart
    - will be checked that every file exists in cache, if not - will be created task to cache it
    - task id transmitted back to user and saves into cookies
    - js script will check task status periodically untill it will be success or fails. In case when task fails, will be shown popup with error message

Downloading metadata
====================

File with metadata collected from xml files stored in cart cache with analysis ids which stored in cart.

.. autofunction:: cghub.apps.cart.utils.join_analysises