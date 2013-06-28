:tocdepth: 2

API Documentation
=================

.. _api:

Main Interface
--------------

All functionality is implemented in function ``wsapi.api``.

wsapi.api
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: wsapi.api.request_page

.. autofunction:: wsapi.api.request_ids

.. autofunction:: wsapi.api.request_details

.. autofunction:: wsapi.api.item_details

.. autofunction:: wsapi.api.item_xml

.. _settings:

Settings
--------------

Settings dict can be passed to ``request_page``, ``request_ids``, ``request_details``, ``item_details`` or ``item_xml`` function:

.. code-block:: python

    hits, results = request_page(query=query, limit=10,
                        settings={
                            'CGHUB_SERVER': 'https://cghub.ucsc.edu',
                            'CGHUB_ANALYSIS_ID_URI': '/cghub/metadata/analysisId'})

In case, when some settings not specified, will be used default settings, specified in `wsapi/settings.py`.

.. automodule:: wsapi.settings
    :members:
    :undoc-members:
    :show-inheritance:


Exceptions
-------------

.. automodule:: wsapi.exceptions
    :members:
    :undoc-members:
    :show-inheritance:


Utility functions
-------------------

``wsapi.utils.urlopen`` should be used instead of ``urllib2.urlopen``.

.. automodule:: wsapi.utils
    :members:
    :undoc-members:
    :show-inheritance:
