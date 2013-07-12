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
    mkdir pids

    # either
    mkvirtualenv -r requirements.txt cghub
    # or (if not using virtualenvwrapper)
    pip install -r requirements

    make syncdb
    make celeryd

    # in another terminal from `cghub` directory
    make run

-----------------------
Filters customizing
-----------------------

Filters list can be edited in ``cghub/apps/core/filters_storage_full.py``:

.. code-block:: python

    ALL_FILTERS = OrderedDict([
    ("study", {
        "title": "By Study",
        "filters": OrderedDict([
            ("phs000178", "TCGA"),
            ('TCGA_MUT_BENCHMARK_4', 'TCGA Benchmark'),
        ])
    }),
    ("center_name", {
        "title": "By Center",
        ...

In case of refassem_short_name, complex queries with "OR" are allowed:

.. code-block:: python

    ('refassem_short_name', {
        'filters': OrderedDict([
            ('NBCI36* OR HG18*', 'NBCI36/HG18'),
            ('GRCh37* OR HG19*', 'GRCh37/HG19'),
        ]),
        'title': 'By Assembly',
    }),

----------------------------
Filters list shortening
----------------------------

There are many possible options for filters in the sidebar. Not all of them are used by CGHub. To reduce the list a management command ``selectfilters`` is written. It should be used as following:

.. code-block:: bash

    $ python manage.py selectfilters

``selectfilters`` management command first trying to obtain data for existing filters.
If no results returns, filter will be removed.
In case when sum of results for every filter will be less than count of all results, all filters will be found by recursive search.

This is a part of ``selectfilters`` management command output, it can help to understand how it works:

.. code-block:: bash

    Checking filters
    Checking disease_abbr filters
    - Filter ACC ... removed
    - Filter BLCA ... added
    - Filter BRCA ... added
    - Filter CESC ... added
    - Filter CNTL ... added
    - Filter COAD ... added
    - Filter DLBC ... added
    - Filter ESCA ... added
    - Filter GBM ... added
    - Filter HNSC ... added
    - Filter KICH ... added
    - Filter KIRC ... added
    - Filter KIRP ... added
    - Filter LAML ... added
    - Filter LCLL ... added
    ...
    Some other filters for disease_abbr exists (150 from 47928).
    Searching for other filters ...
    Searching [disease_abbr=A*]
    - Found 0
    Searching [disease_abbr=B*]
    - Found 6640
    Searching [disease_abbr=BA*]
    - Found 0
    ...
    Searching [disease_abbr=C*]
    - Found 4336
    Searching [disease_abbr=CA*]
    - Found 0
    Searching [disease_abbr=CB*]
    - Found 0
    Searching [disease_abbr=CC*]
    - Found 0
    Searching [disease_abbr=CD*]
    - Found 0
    Searching [disease_abbr=CE*]
    - Found 667
    Searching [disease_abbr=CF*]
    - Found 0
    Searching [disease_abbr=CG*]
    - Found 0
    Searching [disease_abbr=CH*]
    - Found 0
    Searching [disease_abbr=CI*]
    - Found 0
    Searching [disease_abbr=CJ*]
    - Found 0
    Searching [disease_abbr=CK*]
    - Found 0
    Searching [disease_abbr=CL*]
    - Found 0
    Searching [disease_abbr=CM*]
    - Found 0
    Searching [disease_abbr=CN*]
    - Found 25
    Searching [disease_abbr=CO*]
    - Found 3644
    Searching [disease_abbr=D*]
    - Found 132
    Searching [disease_abbr=E*]
    - Found 62
    ...
    Searching [disease_abbr=ST*]
    - Found 2137
    Searching [disease_abbr=T*]
    - Found 3079
    Searching [disease_abbr=U*]
    - Found 3136
    Checking sample_type filters
    - Filter 07 ... removed
    - Filter 05 ... removed
    - Filter 10 ... added
    - Filter 14 ... added
    - Filter 12 ... added
    - Filter 61 ... removed
    - Filter 50 ... added
    - Filter 20 ... added
    - Filter 13 ... added
    - Filter 08 ... removed
    - Filter 06 ... added
    - Filter 09 ... removed
    - Filter 03 ... added
    - Filter 01 ... added
    - Filter 60 ... removed
    - Filter 02 ... added
    - Filter 04 ... removed
    - Filter 40 ... removed
    - Filter 11 ... added
    Checking analyte_code filters
    - Filter D ... added
    - Filter G ... removed
    - Filter H ... added
    - Filter R ... added
    - Filter T ... added
    - Filter W ... added
    - Filter X ... added
    ...
    Removing those filters that are not used ...
    - Removed disease_abbr:ACC
    - Removed disease_abbr:LCML
    - Removed disease_abbr:MISC
    - Removed disease_abbr:PCPG
    - Removed disease_abbr:UCS
    - Removed disease_abbr:UVM
    - Removed sample_type:07
    ...
    Adding new filters ...
    - Added new filter disease_abbr:NBL
    ! Please add this filter to filters_storage_full.py
    Wrote to /home/nanvel/projects/ucsc-cghub/cghub/apps/core/filters_storage.json.

NBL will be added to filters_storage.json:

.. code-block:: bash

    ...
    "MESO": "Mesothelioma", 
    "MM": "Multiple Myeloma Plasma cell leukemia", 
    "NBL": "NBL", 
    "OV": "Ovarian serous cystadenocarcinoma", 
    "PAAD": "Pancreatic adenocarcinoma",

To change NBL name, You should add this filter to filters_storage_full.py and reexecute ``selectfilters`` command.

Filters list can be accessed from ``filters_storage.py``, where automatically creates ALL_FILTERS variable and populates by data stored in ``filters_storage.json``. If ``filters_storage.json`` will be missed, then ``filters_storage.json.default`` will be used instead.

------
Celery
------

We use Celery for periodic tasks (only caching for now). 

`Celery <http://www.celeryproject.org/>`__ - distributed task queue.

From celery documentatin:
The execution units, called tasks, are executed concurrently on a single or more worker servers using multiprocessing, Eventlet, or gevent. Tasks can execute asynchronously (in the background) or synchronously (wait until ready).

Celery requires a solution to send and receive messages, usually this comes in the form of a separate service called a message broker. The most popular is `RabbitMQ <http://www.rabbitmq.com/>`__.

We use `djcelery <https://github.com/celery/django-celery>`__ for integratin celery to django. It provides using the Django ORM and cache backend for storing results, autodiscovery of task modules for applications listed in INSTALLED_APPS, and more.

--------
RabbitMQ
--------

As message broker for Celery we use RabbitMQ.

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
