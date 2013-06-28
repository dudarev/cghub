.. About using the API

Usage
============================================

.. _wsi-api:

WSI API
-----------

Web service interface (WSI) to CGHub data is described in `CGHub documentation <https://cghub.ucsc.edu/help/help.html>`__
(look for `User's Guide`).
The Python API described in this documentation provides Python interface to it.

At the moment WSI API provides several metadata resources (``analysisId``, ``analysisDetail``, 
``analysisSubmission``, ``analysisFull``, ``analysisObject``, ``analysisAttributes``)

In the Python API wrapper ``analysisId``, ``analysisDetail`` and ``analysisFull`` are used now.
One may see example of possible responses for a specific id with HTTP requests as shown below:

https://cghub.ucsc.edu/cghub/metadata/analysisId?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

https://cghub.ucsc.edu/cghub/metadata/analysisDetail?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

https://cghub.ucsc.edu/cghub/metadata/analysisFull?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

Data can be returned in json or xml format.

The later returns more details for each query, while the former returns just enough information that could be used
by the download program.

Using Python API
---------------------

For more details see :ref:`API documentation <api>`.

Example:

.. code-block:: python

    from wsapi import QueryRequired
    from wsapi import request_page

    try:
        request_page()
    except QueryRequired:
        print 'request takes either query or file_name parameter'

    hits, results = request_page(query='all_metadata=TCGA-04-1337-01A-01W-0484-10', offset=0, limit=10)
    print hits
    print results
    '''
    Output:
    request takes either query or file_name parameter
    2
    [{u'upload_date': u'2011-03-13T08:00:00Z', u'center_name': u'BCM',
    u'aliquot_id': u'2e66cec2-3607-42bd-92a0-663acbdff603',
    ...}, {..., u'published_date': u'2011-06-17T07:00:00Z',
    u'analysis_full_uri': u'https://stage.cghub.ucsc.edu/cghub/metadata/analysisFull/55c0d3e7-b6e8-40d4-8a3e-73771a747c95'}]
    '''

.. code-block:: python

    from wsapi import requst_details

    def callback(data):
        print data

    hits = request_details(query='all_metadata=TCGA-04-1337-01A-01W-0484-10')
    print hits
    '''
    Output:
    {u'upload_date': u'2011-03-13T08:00:00Z', u'center_name': u'BCM',
    u'analysis_full_uri': u'https://stage.cghub.ucsc.edu/cghub/metadata/analysisFull/916d1bd2-f503-4775-951c-20ff19dfe409', ...}
    {..., u'Result': u'https://stage.cghub.ucsc.edu/cghub/data/analysis/download/55c0d3e7-b6e8-40d4-8a3e-73771a747c95\n\t', 
    u'published_date': u'2011-06-17T07:00:00Z', u'Query': u'all_metadata:TCGA-04-1337-01A-01W-0484-10'}
    2
    '''

All available functions:
    - ``request_page(query, offset=None, limit=None, sort_by=None, settings={})``
    - ``request_ids(query, sort_by=None, settings={})``
    - ``request_details(query, callback, sort_by=None, settings={})``
    - ``item_details(analysis_id, with_xml=False, settings={})``
    - ``item_xml(analysis_id, with_short=False, settings={})``
