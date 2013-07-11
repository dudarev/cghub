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
    from wsapi import Request

    try:
        Request()
    except QueryRequired:
        print 'request takes either query or file_name parameter'

    result = Request(query='all_metadata=TCGA-04-1337-01A-01W-0484-10', offset=0, limit=10)
    print result.hits
    print result.results
    '''
    Output:
    request takes either query or file_name parameter
    2
    [{u'upload_date': u'2011-03-13T08:00:00Z', u'center_name': u'BCM',
    u'aliquot_id': u'2e66cec2-3607-42bd-92a0-663acbdff603',
    ...}, {..., u'published_date': u'2011-06-17T07:00:00Z',
    u'analysis_full_uri': u'https://stage.cghub.ucsc.edu/cghub/metadata/analysisFull/55c0d3e7-b6e8-40d4-8a3e-73771a747c95'}]
    '''
