.. About using the API

Compiling CSS and JS
============================================

LESS is used to maintain stylesheets.
Client side LESS compilator is used in developement environment.

Some requirements should be satisfied to compile static files from LESS
to CSS and Javascript minification for production environment.

Install both nodejs and npm either via packages

https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager

or directly from

http://nodejs.org and http://npm.org

.. code-block:: bash

    curl http://npmjs.org/install.sh | sh

Install grunt:

.. code-block:: bash

    sudo npm install -g grunt

Install grunt-less:

.. code-block:: bash

    sudo npm install -g grunt-less

To compile from LESS to CSS use ``less`` target:

.. code-block:: bash

    make less

To minify js use ``minjs`` target:

.. code-block:: bash

    make minjs
