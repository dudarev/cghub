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
    <div class="someclass js-common-tooltip" data-key="some-key">Some content</div>

    # help.py:
    HELP_HINTS = {
        'common:some-key': 'Some hint' 

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
    - `cghub/apps/cart/tasks.py`

There are next tasks:

.. autofunction:: cghub.apps.cart.tasks.cache_results_task

.. autofunction:: cghub.apps.cart.tasks.add_files_to_cart_by_query

.. _caching:

Caching
=======

There are next types of cache files:
    - cart cache
        - cached files for one analysis id, used when collecting metadata, manifest of summary file. Adds when adding files to cart if not exists yet. Can be saved few versions of files for different last_modified. Path to these files calculated using next pattern: ``{CART_CACHE_DIR}/{analysis_id[:2]}/{analysis_id[2:4]}/{analysis_id}/{last_modified}/analysis[Full|Short].xml``

Folders where cache should be stored specified in settings (CART_CACHE_DIR).

Cart cache
----------

When user adds some files to cart, this files will be saved to cache if they not exists here yet (using cache_results_task).
For every added file will be created two files in cache: one is analysisFull.xml and second is analysisShort.xml that contains only most necessary attributes and used to build manifest file. analysisShort.xml produced from analysisFull by removing some attributes, see 'wsapi.api.Results.remove_attributes'.

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
    - when user click on 'Add to cart' button, attributes values for selected items that stored in table transmitted
    - obtained items data saves to cart (stored in Session)
    - if cart cache file for some of added items not exists yet, will be created task to create it.

Adding all files to cart
------------------------

Here are next sequence of actions:
    - when user click 'Add all to cart' button, current query will be sended to server
    - if amount of files to add to cart will be more then ``settings.MANY_FILES``, will be shown confirmation popup for confirming the number
    - all ids for specified query will be added to cart immediately (for example, cart content will be extended by: {'000f332c-7fd9-4515-bf5f-9b77db43a3fd': {'analysis_id': '000f332c-7fd9-4515-bf5f-9b77db43a3fd'}, '0009cf7a-c9a8-4551-80f6-71d58af6ab72': {'analysis_id': '0009cf7a-c9a8-4551-80f6-71d58af6ab72'}, ...}). It takes much less time than obtaining all data.
    - when id adds to cart, will be checked is cart cache file exists for this item. If not - will be created task to add cart cache for this item.
    - if user opens cart page when it contains only ids, data for this certain page will be downloaded from server and displayed
    - after ids added to cart, will be created task to obtain full data for specified query and fill cart by all necessary attributes (for example, '000f332c-7fd9-4515-bf5f-9b77db43a3fd': {'analysis_id': '000f332c-7fd9-4515-bf5f-9b77db43a3fd'} should become '000f332c-7fd9-4515-bf5f-9b77db43a3fd': {'analysis_id': '000f332c-7fd9-4515-bf5f-9b77db43a3fd', 'satte': 'live', 'study': 'phs000178', ...}). Adding more data to cart performs by callback function that calls every time when an entire result is obtained by sax parser from cghub server. So, no intermediate data stored.
    - this task id is returned back to user in response and saved into cookies
    - js script will checks task status periodically until it will become success or fails. In case when task fails, will be shown popup with error message, otherwise task id will be removed from cookies (if current page is cart page, it will be reloaded)

Task ids for obtaining all data to add to cart calculates from query and session key. This implemented to restrict executing the same tasks by one user. Before adding new task, we checks is this task was created before. If task exists, but it already done (task.state not in (states.RECEIVED, states.STARTED)) we reexecute task (change task.status to states.RETRY before), else, if task not done yet, we redirect user to cart page with no action. If task not exists, we create it.

Manual tasks ids generating also necessary because of it allows to obtain task.id and save it to session before task will be created (and possible launched).

Task ids for saving files to cart cache creates in same manner. It is necessary to avoid duplicating tasks to obtain files for the same item.

Cart data is stored in user session. Session saves to database if it was changed every time when response returned by server. But in django view for adding files to cart we manage session manually: create it if it not exists and save. This decision become because of we need to have current session id to give it to task, but session, if it was not exist before, we'll obtain it unique id only after django view code will be executed.

Default ``settings.MANY_FILES`` located in ``cghub/settings/variables.py``.

User will be unable to remove items from cart, clear cart or sort items in cart until all files are loaded to cart.

If celery will not working, all tasks will be executes as simple functions.

Batch search
============

This feature allows to enter list of ids (analysis_id, aliquot_id, legacy_sample_id, participant_id or sample_id) separated by whitespace or newline, or submit file that contains list of ids and add corresponding items to cart.

First, search will be done by analysis_id, if results will be found not for all ids, will be done search by aliquot_id, participant_id and sample_id.

If some ids matches legacy_sample_id pattern, will be done search by legacy_sample_id.

User has 2 choices:
    - immediately add all found items to cart
    - show search results before adding them to cart


Downloading metadata
====================

File with metadata collected from xml files stored in cart cache with analysis ids which stored in cart.

Pieces of data
==============

Used URI's
----------

AnalysisId:
    - used by wsapi.Request if wsapi.Request.only_ids == True

AnalysisDetail:
    - used by wsapi.Request

AnalysisFull:
    - used by wsapi.Request if wsapi.Request.full == True


Displayed attributes
--------------------

    - aliquot_id (Aliquot id)
    - analysis_id (Analysis Id)
    - analyte_code (Experiment Type)
    - center_name (Center)
    - disease_abbr (Disease)
    - filesize (used to calculate Files Size)
    - last_modified (Last modified)
    - legacy_sample_id (Barcode)
    - library_strategy (Library Type)
    - participant_id (Participant id)
    - platform (Platform)
    - published_date (Published time)
    - refassem_short_name (Assembly)
    - sample_accession (Sample Accession)
    - sample_id (Sample id)
    - sample_type (Sample Type)
    - state (State)
    - study (Study)
    - tss_id (TSS id)
    - upload_date (Uploaded)

Custom fields
=============

Custom fields can be added by overriding wsapi.Request.patch_result method.

Next custom fields were added:

    - files_size
    - checksum
    - filename

See ``cghub/apps/core/utils.py``.

.. code-block:: python

    class WSAPIRequest(Request):
        """
        Override patch_result method to add custom fields.
        """

        def patch_result(self, result):
            # files_size_field
            files_size = 0
            for f in result['files']:
                files_size += f['filesize']
            result['files_size'] = files_size
            # checksum
            if result['files']:
                result['checksum'] = result['files'][0]['checksum']['#text']
                result['filename'] = result['files'][0]['filename']
            else:
                result['checksum'] = None
                result['filename'] = None
            return result
