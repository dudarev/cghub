.. 

Dependencies
============================================

-----
lxml
-----

The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API.

Here we also use its alternative API -- `lxml.objectify <http://lxml.de/objectify.html>`__

- http://lxml.de/
- http://lxml.de/objectify.html

--------
RabbitMQ
--------

Message broker for Celery.

Installing from the APT repository
----------------------------------

Add the following line to your /etc/apt/sources.list:

	``deb http://www.rabbitmq.com/debian/ testing main``

(Please note that the word testing in this line refers to the state of our release of RabbitMQ, not any particular Debian distribution. You can use it with Debian stable, testing or unstable, as well as with Ubuntu. We describe the release as "testing" to emphasise that we release somewhat frequently.)

(optional) To avoid warnings about unsigned packages, add our public key to your trusted key list using apt-key(8):

.. code-block:: bash

	$ wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
	$ sudo apt-key add rabbitmq-signing-key-public.asc

Run 

.. code-block:: bash

	$ apt-get update.

Install packages as usual; for instance,

.. code-block:: bash

	$ sudo apt-get install rabbitmq-server

Setting up RabbitMQ
-------------------

To use celery we need to create a RabbitMQ user, a virtual host and
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

------
Celery
------

Installation
------------
You can install Celery either via the Python Package Index (PyPI).

To install using pip:

.. code-block:: bash

	$ pip install -U Celery


Configuring
-----------

If you're using wsapi with django, you can configure the celery in more convinient way with
th ``django-celery`` library, see
http://docs.celeryproject.org/en/latest/django/index.html

If you're using the default loader, you must create the :file:`celeryconfig.py`
module and make sure it is available on the Python path. Example:

.. code-block:: python

	import settings

	CELERY_IMPORTS = ("tasks",)

	CELERYBEAT_SCHEDULE = {
	    "clear-api-cache": {
	        "task": "tasks.api_cache_clear_task",
	        "schedule": settings.TIME_CHECK_API_CACHE_INTERVAL,
	    },
	}

	CELERY_RESULT_BACKEND = "amqp"

	CELERYD_CONCURRENCY = 1

	# $ rabbitmqctl add_user myuser mypassword
	# $ rabbitmqctl add_vhost myvhost
	# $ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
	# Example
	# BROKER_URL = "amqp://user:password@host:port/vhost"
	# guest user if for example only

	BROKER_URL = "amqp://guest:guest@localhost:5672//"