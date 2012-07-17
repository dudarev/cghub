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

    # access to attributes
    # <EXPERIMENT_REF accession="SRX074784" refcenter="BI" refname="7290.WR24924.Catch-62054.B045FABXX110327.P"/>

    first_run_experiment_ref = results.Result[0].run_xml.RUN_SET[0].RUN[0].EXPERIMENT_REF
    refname = first_run_experiment_ref.attrib['refname']
