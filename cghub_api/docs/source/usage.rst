.. About using the API

Usage
============================================

.. _wsi-api:

WSI-API
-----------

A short description of WSI-API.

TODO: more details about WSI, in particular, getting results with attributes.

Using Python API
---------------------

For more details see :ref:`API documentation <api>`.

Example:

.. code-block:: python

    from cghub_api.exceptions import QueryRequired
    from cghub_api.api import request

    try:
        request()
    except QueryRequired:
        print 'request takes either query or file_name parameter'

    results = request(file_name='tests/test_data/aliquot_id.xml')
    first_experiment_title = results.Result[0].experiment_xml.EXPERIMENT_SET[0].EXPERIMENT[0].TITLE
    first_analysis_title = results.Result[0].analysis_xml.ANALYSIS_SET[0].ANALYSIS[0].TITLE

    # access to attributes
    # <EXPERIMENT_REF accession="SRX074784" refcenter="BI" refname="7290.WR24924.Catch-62054.B045FABXX110327.P"/>

    first_run_experiment_ref = results.Result[0].run_xml.RUN_SET[0].RUN[0].EXPERIMENT_REF
    refname = first_run_experiment_ref.attrib['refname']

Caching
~~~~~~~

All requests to the external server are cached. They are saved in the form of files in ``CACHE_DIR`` which is defined in :ref:`settings`. 
It is a good idea to clean cache once in a while with :func:`cghub_api.utils.clear_cache`. 
Here is an example of using it with periodic Celery task:

.. code-block:: python

    import datetime
    from datetime import timedelta

    from celery.task import task

    from cghub_api.utils import clear_cache

    TIME_DELETE_API_CACHE_FILES_OLDER = timedelta(hours=2)

    @task(ignore_result=True)
    def api_cache_clear_task():
        """
        Task to clear API cache which is by default is stored in
        ``/tmp/cghub_api/``.
        """
        now = datetime.datetime.now()
        clear_cache(now - TIME_DELETE_API_CACHE_FILES_OLDER)
