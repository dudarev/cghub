:tocdepth: 2

API Documentation
=================

.. _api:

Main Interface
--------------

All functionality is implemented in function ``wsapi.Request``.

wsapi.api
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: wsapi.api.Request
    :members:
    :undoc-members:
    :member-order: bysource

    .. automethod:: wsapi.api.Request.__init__


.. _settings:

Settings
--------------

Settings dict can be passed to wsapi.api.Request:

.. code-block:: python

    result = Request(query=query, limit=10,
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
