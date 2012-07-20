Settings
=================

Celery
----------

To run periodic tasks (for now only related to :ref:`caching <cacing>`) we use Celery.
Its settings are in ``settings/celery_settings.py``.

For the moment we are using database as messages queue:

http://docs.celeryproject.org/en/latest/getting-started/brokers/django.html#broker-django

This probably should be changed in the future to more robust RabbitMQ.

.. _caching:

Caching
---------

Two types of caching is used:

1. Requests are cached by the API.
2. When items are added to the cart, requests are made to save XML for each result.

API cache
~~~~~~~~~~~~~

API does not clean cache automatically. Celery task to do so is scheduled to run. Its parameters are stored in ``settings/api_cache.py``:

.. code-block:: python

    # api_cache.py

    TIME_DELETE_API_CACHE_FILES_OLDER = timedelta(hours=2)
    TIME_CHECK_API_CACHE_INTERVAL = timedelta(hours=1)

They control how often the task is ran (1 hour above) and how old files are kept (2 hours). 
The directory where the cache is kept is defined in the API settings (``/tmp/cghub_api/`` by default).

Cart cache
~~~~~~~~~~~~~~~

When a result is added to the cart a request to get its XML is made to external server, 
so that XML could be quickly served when requested. It has similar parameters. The directory
to keep files is also specified.

.. code-block:: python

    # cart_cache.py

    CART_CACHE_FOLDER = os.path.join(MEDIA_ROOT, 'api_results_cache')
    TIME_DELETE_CART_CACHE_FILES_OLDER = timedelta(hours=24)
    TIME_CHECK_CART_CACHE_INTERVAL = timedelta(hours=12)

Paging
-------------

The results are paged when requested from the server. This paging is done by the app, not by WSI API. 
Number of results per page may be set in ``settings/defaults.py``:

.. code-block:: python

    # default.py

    DEFAULT_PAGINATOR_LIMIT = 10

