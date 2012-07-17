:tocdepth: 2

API Documentation
=================

.. _api:

Main Interface
--------------

All functionality is implemented in function :func:`cghub_api.api.request`. It returns object of class :class:`cghub_api.api.Results`.

cghub_api.api
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: cghub_api.api.request

.. autoclass:: cghub_api.api.Results
    :members:
    :undoc-members:
    :member-order: bysource

    .. automethod:: cghub_api.api.Results.__init__

.. _configuration

Settings
--------------

At the moment the only setting is location of the directory where request files are cached.

.. automodule:: cghub_api.settings
    :members:
    :undoc-members:
    :show-inheritance:

Exceptions
-------------

.. automodule:: cghub_api.exceptions
    :members:
    :undoc-members:
    :show-inheritance:


Utility functions
-------------------

Only one utility function at the moment to clean cache.

.. automodule:: cghub_api.utils
    :members:
    :undoc-members:
    :show-inheritance:
