.. About using the API

Usage
============================================

Based on current tests:

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
