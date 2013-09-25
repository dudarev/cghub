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

Caching
=======

There are next types of cache files:
    - cart cache
        - cached files for one analysis id, used when collecting metadata, manifest of summary file. Adds when adding files to cart if not exists yet. Can be saved few versions of files for different last_modified. Path to these files calculates using next pattern: ``{FULL_METADATA_CACHE_DIR}/{analysis_id[:2]}/{analysis_id[2:4]}/{analysis_id}/{last_modified}/analysis.xml``

Folder where cart cache should be stored specified in settings (FULL_METADATA_CACHE_DIR).

Cart cache
----------

When user adds some files to cart, this files will be saved to cache if they not exists here yet (creates on Analysis create signal).

Path to analysis file can be obtained by next function:

.. autofunction:: cghub.apps.cart.cache.get_analysis_path

To get cghub_python_api.api.Result object for specified analysis_id and last_modified can be used next function:

.. autofunction:: cghub.apps.cart.cache.get_analysis

If file will be not  cached, application will try to download it. In case when file with specified analysis_id for specified last_modified will be not found, AnalysisFileException exception will be raised.

``update_full_metadata_cache`` management command can be used to download all non existent or outdated cache.
It works next way:
    - make request to analysisDetail uri
    - check that all Analysis objects exists and recent
    - if some analysis is outdated, it will be updated
    - if analysis does not exists, it will be added
    - cache existance will be checked for every Analysis object
    - if cache does not exists, it will be downloaded

Adding files to cart
====================

There are two ways to add items to cart:
    - select few items and add them to cart
    - add all items obtained by specified query

Adding selected files to cart
-----------------------------

The following sequence of actions are performing:
    - when user click on 'Add to cart' button, attributes values for selected items that stored in table transmitted
    - corresponding Analysises will be added to cart
    - if some analysis would be not found, it will be downloaded. If it appears that last_modified time was changed, Analysis will be updated

Adding all files to cart
------------------------

Here are next sequence of actions:
    - when user click 'Add all to cart' button, current query will be sended to server
    - if amount of files to add to cart will be more then ``settings.MANY_FILES``, will be shown confirmation popup for confirming the number
    - will be done request to obtain all analysisDetail for specified query and for all result will be added corresponding analysis Analysis.
    - If Analysis not exists, it will be created. If last_modified time was changed, it Analysis will be updated


Cart data is stored in database. There are 3 models used: Cart, Analysis, CartItem. Analysis is unique for analysis_id. It stores analysis_id, last_modified, state and files_size. On Analysis update cart cache updates automatically. Cart creates and removes synchronously with user Session table. CartItem connects Cart and Analysises.

Default ``settings.MANY_FILES`` located in ``cghub/settings/variables.py``.


Search by query
===============

First, will be attempt to find results by aliquot_id, analysis_id,
participant_id, sample_id and legacy_sample_id.
If Results will be found, they will be displayed. Otherwise, will be done search by xml_text (in this case warning message will be shown).
Is some filters are selected, they will be used.

Batch search
============

This feature allows to enter list of ids (analysis_id, aliquot_id, legacy_sample_id, participant_id or sample_id) separated by whitespace or newline, or submit file that contains list of ids and add corresponding items to cart.

First, search will be done by analysis_id, if results will be found not for all ids, will be done search by aliquot_id, participant_id and sample_id.

If some ids matches legacy_sample_id pattern, will be done search by legacy_sample_id.

After search is done, will be shown search stats and results table.
User can remove some items from table or add all items to cart.


Downloading metadata
====================

File with metadata collected from xml files stored in cart cache with analysis ids which stored in cart.
If file would be not found in cache, it will be downloaded.

Pieces of data
==============

Used URI's
----------

AnalysisId:
    - used by cghub.apps.core.utils.RequestIDs

AnalysisDetail:
    - used by cghub.apps.core.utils.RequestDetail

AnalysisFull:
    - used by cghub.apps.core.utils.RequestFull


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

Custom fields can be added by overriding cghub_python_api.Request* methods.

Next custom fields were added:

    - files_size
    - checksum
    - filename

See ``cghub/apps/core/utils.py``.

.. code-block:: python

    class RequestBase(WSAPIRequest):

        def patch_result(self, result, result_xml):
            new_result = {}
            for attr in ATTRIBUTES:
                if result[attr].exist:
                    new_result[attr] = result[attr].text
            new_result['filename'] = result['filename.0'].text
            try:
                new_result['files_size'] = int(result['filesize.0'].text)
            except TypeError:
                new_result['files_size'] = 0
            new_result['checksum'] = result['checksum.0'].text
            return new_result
