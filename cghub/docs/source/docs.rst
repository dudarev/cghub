.. About writing and using the documentation

Updating documentation
============================================

Update files in the ``source`` directory. Build html pages with ``make html`` command.

The following line was added to Sphynx Makefile:

.. code-block:: Makefile

    serve:
            cd build/html/ && python -m SimpleHTTPServer 8002

It allows to call ``make serve`` and examine the documentation at http://localhost:8002
