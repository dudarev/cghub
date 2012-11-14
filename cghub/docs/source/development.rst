.. About development

Development
============================================

-------------------------------
Setting up and running the app
-------------------------------

Make sure RabbitMQ server is installed (see section about RabbitMQ below).

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

----------------------------
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

--------
RabbitMQ
--------

We use Celery for periodic tasks (only caching for now). As message broker for Celery we use RabbitMQ.

Installing from the APT repository for Debian/Ubuntu
----------------------------------------------------

As described in `RabbitMQ docs <http://www.rabbitmq.com/install-debian.html>`__:

Add the following line to your ``/etc/apt/sources.list``: ``deb http://www.rabbitmq.com/debian/ testing main``

(Please note that the word testing in this line refers to the state of our release of RabbitMQ, not any particular Debian distribution. You can use it with Debian stable, testing or unstable, as well as with Ubuntu. We describe the release as "testing" to emphasise that we release somewhat frequently.)

(optional) To avoid warnings about unsigned packages, add our public key to your trusted key list using apt-key(8):

.. code-block:: bash

    $ wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
    $ sudo apt-key add rabbitmq-signing-key-public.asc

Run 

.. code-block:: bash

    $ sudo apt-get update

Install packages as usual; for instance,

.. code-block:: bash

    $ sudo apt-get install rabbitmq-server

Setting up RabbitMQ
-------------------

To use Celery we need to create a RabbitMQ user, a virtual host and
allow that user access to that virtual host:

.. code-block:: bash

    $ rabbitmqctl add_user myuser mypassword

.. code-block:: bash

    $ rabbitmqctl add_vhost myvhost

.. code-block:: bash

    $ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

See the RabbitMQ `Admin Guide`_ for more information about `access control`_.

.. _`Admin Guide`: http://www.rabbitmq.com/admin-guide.html

.. _`access control`: http://www.rabbitmq.com/admin-guide.html#access-control

-----------------------
Daemonizing Celery
-----------------------

If you want to daemonize celery, you may use scripts provided by celery itself.
Installation:

.. code-block:: bash

    $ wget https://raw.github.com/celery/celery/master/extra/generic-init.d/celeryd https://raw.github.com/celery/celery/master/extra/generic-init.d/celerybeat https://raw.github.com/celery/celery/master/extra/generic-init.d/celeryevcam
    $ chmod 755 celeryd celerybeat celeryevcam
    $ sudo mv celeryd /etc/init.d/celeryd 
    $ sudo mv celerybeat /etc/init.d/celerybeat
    $ sudo mv celeryevcam /etc/init.d/celeryevcam
    $ sudo touch /etc/default/celeryd
    $ sudo vim /etc/default/celeryd

Change to your paths:

.. code-block:: bash

    # /etc/default/celeryd

    # Name of nodes to start, here we have a single node
    CELERYD_NODES="w1"
    # or we could have three nodes:
    #CELERYD_NODES="w1 w2 w3"

    # Where to chdir at start. Location of manage.py
    CELERYD_CHDIR="/path/to/project"

    # Python interpreter from virtual environment.
    ENV_PYTHON="path/to/env/bin/python"

    # How to call "manage.py celeryd_multi"
    CELERYD_MULTI="$ENV_PYTHON $CELERYD_CHDIR/manage.py celeryd_multi"

    # How to call "manage.py celeryctl"
    CELERYCTL="$ENV_PYTHON $CELERYD_CHDIR/manage.py celeryctl"

    # Extra arguments to celeryd
    CELERYD_OPTS="-E --time-limit=300 --concurrency=8"

    # Name of the celery config module.
    CELERY_CONFIG_MODULE="cghub.settings"

    # %n will be replaced with the nodename.
    CELERYD_LOG_FILE="/path/to/logs/dir/%n.log"
    CELERYD_PID_FILE="/path/to/pids/dir/%n.pid"

    # Workers should run as an unprivileged user.
    CELERYD_USER="celery"
    CELERYD_GROUP="celery"

    # Name of the projects settings module.
    export DJANGO_SETTINGS_MODULE="cghub.settings"

    # Where the Django project is.
    CELERYBEAT_CHDIR="/path/to/project"

    # Path to celerybeat
    CELERYBEAT="$ENV_PYTHON $CELERYD_CHDIR/manage.py celerybeat"

    # Extra arguments to celerybeat
    CELERYBEAT_OPTS="--schedule=/var/run/celerybeat-schedule"

    CELERYBEAT_PID_FILE="/path/to/logs/dir/celerybeat.pid"
    CELERYBEAT_LOG_FILE="/path/to/logs/dir/celerybeat.log"

    # Path to celeryd
    CELERYEV="$ENV_PYTHON $CELERYD_CHDIR/manage.py"

    # Extra arguments to manage.py
    CELERYEV_OPTS="celeryev"

    # Camera class to use (required)
    CELERYEV_CAM="djcelery.snapshot.Camera"

    CELERYEV_PID_FILE="/path/to/pids/dir/celeryevcam.pid"
    CELERYEV_LOG_FILE="/path/to/logs/dir/celeryevcam.log"

Note that if you want Django to monitor tasks (in the admin panel or at the status page provided by the cghub app) you need to start celeryd with "-E" argument to create events and start /etc/init.d/celeryevcam daemon.

Also if you choose to run as unprivileged user ``celery``, make sure to create it and change permissions of all required directories

.. code-block:: bash
    
    $ sudo adduser --system --no-create-home --disabled-login --disabled-password --group celery

.. code-block:: bash

    sudo chown celery:celery /var/run/celery/
    sudo chown celery:celery /tmp/wsapi/

Start daemons:

.. code-block:: bash

    $ sudo /etc/init.d/celeryd start
    $ sudo /etc/init.d/celerybeat start
    $ sudo /etc/init.d/celeryevcam start

Make sure that logs are OK (if you set up ``/path/to/logs/dir`` above as ``/var/log/celery``):

.. code-block:: bash

    $ vim /var/log/celery/w1.log 
    $ vim /var/log/celery/celerybeat.log 
    $ vim /var/log/celery/celeryevcam.log


or just

.. code-block:: bash

    $ vim /var/log/celery/*.log 

On the website check ``/admin/djcelery/workerstate/`` and ``/admin/djcelery/periodictask/`` to see that the worker is online and periodic task are scheduled (you need to see at least two, one for cleaning requests cache, another for cleaning cart cache). You may adjust periodicity there as well.
