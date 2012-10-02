.. About deployment

Testing
============================================

Unit and UI tests are saved in corresponding directories: ``cghub/apps/cart/test``, ``cghub/apps/core/test``, ``cghub/apps/help``.

Unit tests
------------

One may run only unittests by using ``make test`` command. Tests that run only unit tests are specified in ``Makefile.def.default``.

UI Selenium tests
------------------

Run only UI Selenium tests with ``make test_ui`` command. Check ``Makefile.def.default`` for tests that run only Selenium tests.

There were some issues with running Selenium tests with SQLite, 
it may be a good idea to run them with Postgres or MySQL.
For this setup the database and modify local settings in ``local.py``:

.. code-block:: python

    # cghub/settings/local.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'db_name',
            'USER': 'user_name',
            'PASSWORD': 'password',
            'HOST': '',
            'PORT': '',
        }
    }

Plan for UI tests is stored at ``cghub/docs/CGHub-UI-tests-plan.csv``.
