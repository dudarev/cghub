.. About development

Development
============================================

To run the app on localhost:

.. code-block:: bash

    # pay attention to comments

    git clone git@github.com:dudarev/cghub.git cghub
    cd cghub
    cp Makefile.def.default Makefile.def
    cp cghub/settings/local.py.default cghub/settings/local.py
    mkdir {pids,logs}

    # either
    mkvirtualenv -r requirements.txt cghub
    # or (if not using virtualenvwrapper)
    pip install -r requirements

    make syncdb
    make celeryd

    # in another terminal from `cghub` directory
    make run

Filters list shortening
----------------------------

There are many possible options for filters in the sidebar. Not all of them are used by CGHub. To reduce the list a management command ``selectfilters`` is written. It should be used as following:

.. code-block:: bash

    $ python manage.py selectfilters

It takes file ``cghub/apps/core/filters_storage_full.py`` and for every filter stored there checks if results with such filter may be obtained for the API. First it queries for today, then last 7 days and keeps increasing time interval until results are found. If the results are found the filter is copied into ``cghub/apps/core/filters_storage_short.py``, otherwise it is ignored. Also the filters that are already queried are placed into a file, so that the command may be interrupted and started again.

If it is necessary to erase information about filters that were ran use ``-c`` option:

.. code-block:: bash

    $ python manage.py selectfilters -c

**Important:** after the command is ran you need to manually copy ``filters_storage_short.py`` to ``filters_storage.py`` which is used by the app.
