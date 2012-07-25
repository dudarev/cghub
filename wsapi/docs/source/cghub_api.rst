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

.. autoclass:: wsapi.api.Results
    :members:
    :undoc-members:
    :member-order: bysource

    .. automethod:: wsapi.api.Results.__init__

.. _settings:

Settings
--------------

At the moment the only setting is location of the directory where request files are cached.

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

Only one utility function at the moment to clean cache.

.. automodule:: wsapi.utils
    :members:
    :undoc-members:
    :show-inheritance:
