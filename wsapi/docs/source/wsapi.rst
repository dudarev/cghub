:tocdepth: 2

API Documentation
=================

.. _api:

Main Interface
--------------

All functionality is implemented in function :func:`wsapi.api.request`. It returns object of class :class:`wsapi.api.Results`.

wsapi.api
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: wsapi.api.request

.. autofunction:: wsapi.api.multiple_request

.. autofunction:: wsapi.api.merge_results

.. autoclass:: wsapi.api.Results
    :members:
    :undoc-members:
    :member-order: bysource

    .. automethod:: wsapi.api.Results.__init__

.. _settings:

wsapi.api_light
~~~~~~~~~~~~~~~~~~~~

Implementation of the lightweight way to obtain results from cghub server:
    1. obtain ids list for specified query (from cache or
load from CGHUB_ANALYSIS_ID_URI)
    2. load attributes for specified page items (using
CGHUB_ANALYSIS_FULL_URI)

.. autofunction:: wsapi.api_light.request_light

Settings
--------------

Settings dict can be passed to ``request`` or ``multiple_request`` function:

.. code-block:: python

    results = api_request(query=query,
                        settings={
                            'CGHUB_SERVER': 'https://cghub.ucsc.edu',
                            'CGHUB_ANALYSIS_ID_URI': '/cghub/metadata/analysisId'})

In case, when some settings not specified, will be used default settings, specified in `wsapi/settings.py`.

Available settings:
    - CGHUB_SERVER: CGHub server url
    - CGHUB_ANALYSIS_ID_URI: Analysis Object Identification uri
    - CGHUB_ANALYSIS_FULL_URI: Complete set of attributes uri
    - CACHE_DIR: directory to store cache, ``/tmp/wsapi/`` by default
    - USE_CACHE: enables caching if equals True, False is the default
    - CACHE_BACKEND: determines cache type, for now available types are ('simple',)

.. automodule:: wsapi.settings
    :members:
    :undoc-members:
    :show-inheritance:


Cache
--------

.. automodule:: wsapi.cache
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

Only one utility function at the moment to clean cache.

.. automodule:: wsapi.utils
    :members:
    :undoc-members:
    :show-inheritance:
