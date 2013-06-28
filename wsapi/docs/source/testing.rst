.. About testing

Testing
============================================

WSAPI tests
-----------

Automatic unit tests may be launched from root directory with `nose`_:

.. code-block:: bash

    $ nosetests

A few tests make queries to external server (`test_request.py`), but most of them rely on local test files.


WSAPI Testing Mode
------------------

Wsapi can be switched to testing mode, it allows to simplify and speedup testing applications that use wsapi.

To enable testing mode, TESTING_MODE setting should be setted to True.
Also can be specified directory where testing cache will be stored by using TESTING_CACHE_DIR setting.

The main idea of testing mode is that used cached results instead of obtaining them from server in every test.

Example of usage:

.. code-block:: python

    from wsapi import requst_page

    hits, results = request_page(
                query='all_metadata=TCGA-04-1337-01A-01W-0484-10',
                limit=10, settings={'TESTING_MODE': True})

    hits, results = request_page(
                query='all_metadata=TCGA-04-1337-01A-01W-0484-10',
                limit=10, settings={'TESTING_MODE': True})

The second query will be done much faster than the first.

.. _nose: http://nose.readthedocs.org/en/latest/
