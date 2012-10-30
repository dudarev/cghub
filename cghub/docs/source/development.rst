.. About development

Development
============================================

----------------------------
Setting up and running the app:
-------------------------------

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

