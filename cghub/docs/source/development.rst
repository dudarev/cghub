.. About deployment

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
