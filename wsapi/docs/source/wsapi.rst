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
CGHUB_ANALYSIS_ATTRIBUTES_URI)

.. autofunction:: wsapi.api_light.request_light

Settings
--------------

Available settings:

CACHE_DIR - cache files are kept here
USE_CACHE - boolean, enabling or disabling caching
CACHE_BACKEND - string, name of the cache backend that will be used by app.
    For now only 'simple' backend is available(stores cache in files in the CACHE_DIR)
Other available settings see in settings.py file.

For settings customizing use settings_local.py.

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
