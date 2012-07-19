.. About deployment

Deployment
============================================

It should be pretty standard to deploy the site with Apache mod_wsgi, 
see `documentation on Django site <https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/>`__.

Since, we are using Celery to handle caches the ``celeryd`` process should be activated. 
In the example of ``post_deploy.sh`` file local dabase is synced, 
API documentaiton is created,
and ``celeryd`` process is started.

.. code-block:: bash

    # post_deploy.sh
    #!/bin/sh

    rev_path=`pwd`
    config_path=`dirname ${rev_path}`/uwsgi

    # syncdb
    PYTHONPATH="${config_path}:${rev_path}" django-admin.py syncdb --noinput --settings settings_deploy

    # make documentation
    cd ${rev_path}/cghub_api/docs/ && make html

    # start celeryd process
    cd ${rev_path} && make celeryd &

It is a good idea to keep database file (in case of sqlite) outside of the code directory if 

.. code-block:: python

    # settings_deploy.py
    from cghub.settings import *

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '../deploy.sqlite3',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

Local settings
------------------

Local settings in ``cghub/settings/local.py `` need to be updated. An example:

.. code-block:: python

    # cghub/settings/local.py
    import os

    def rel(*x):
            return os.path.normpath(os.path.join(os.path.abspath\
                                            (os.path.dirname(__file__)), *x))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': rel('..', '..', '..', 'deploy.sqlite3'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
