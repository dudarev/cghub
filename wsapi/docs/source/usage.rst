.. About using the API

Usage
============================================

.. _wsi-api:

WSI API
-----------

Web service interface (WSI) to CGHub data is described in `CGHub documentation <https://cghub.ucsc.edu/help.html>`__
(look for `User's Guide`).
The Python API described in this documentation provides Python interface to it.

At the moment WSI API provides several metadata resources (``analysisId``, ``analysisDetail``, 
``analysisSubmission``, ``analysisFull``, ``analysisObject``, ``analysisAttributes``)

In the Python API wrapper ``analysisId`` and ``analysisAttributes`` are used now.
One may see example of possible responses for a specific id with HTTP requests as shown below:

https://cghub.ucsc.edu/cghub/metadata/analysisId?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

https://cghub.ucsc.edu/cghub/metadata/analysisAttributes?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

The later returns more details for each query, while the former returns just enough information that could be used
by the download program.

Some ideas how WSI API may be extended are described in :doc:`future` section.

Using Python API
---------------------

For more details see :ref:`API documentation <api>`.

Example:

.. code-block:: python

    from wsapi.exceptions import QueryRequired
    from wsapi.api import request

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

.. code-block:: python

    >>> from wsapi.api import multiple_request
    >>> mr = multiple_request(queries_list=['xml_text=5c4da*', 'analysis_id=5c4da*'])
    >>> mr
    <wsapi.api.Results object at 0xa7c430c>
    >>> xml = mr._lxml_results
    >>> xml.Hits
    2
    >>> xml.xpath('Query')
    ['analysis_id:5c4da*', 'xml_text:5c4da*']
    >>> xml.xpath('Result/analysis_id')
    ['3f3f1d98-7657-4123-ae60-ff59e5dfd66c', '5c4da821-5329-47bc-8941-88f477afcbf1']

Caching
~~~~~~~

All requests to the external server are cached. They are saved in the form of files in ``CACHE_DIR`` which is defined in :ref:`settings`. 
It is a good idea to clean cache once in a while with :func:`wsapi.utils.clear_cache`. 
Here is an example of using it with a periodic Celery task:

.. code-block:: python

    import datetime
    from datetime import timedelta

    from celery.task import task

    from wsapi.utils import clear_cache

    TIME_DELETE_API_CACHE_FILES_OLDER = timedelta(hours=2)

    @task(ignore_result=True)
    def api_cache_clear_task():
        """
        Task to clear API cache which is by default is stored in
        ``/tmp/wsapi/``.
        """
        now = datetime.datetime.now()
        clear_cache(now - TIME_DELETE_API_CACHE_FILES_OLDER)

An example of :file:`celeryconfig` :

.. code-block:: python

    import settings

    CELERY_IMPORTS = ("tasks",)

    CELERYBEAT_SCHEDULE = {
        "clear-api-cache": {
            "task": "tasks.api_cache_clear_task",
            "schedule": settings.TIME_CHECK_API_CACHE_INTERVAL,
        },
    }

    CELERY_RESULT_BACKEND = "amqp"

    CELERYD_CONCURRENCY = 1

    # $ rabbitmqctl add_user myuser mypassword
    # $ rabbitmqctl add_vhost myvhost
    # $ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
    # Example
    # BROKER_URL = "amqp://user:password@host:port/vhost"
    # guest user if for example only

    BROKER_URL = "amqp://guest:guest@localhost:5672//"
