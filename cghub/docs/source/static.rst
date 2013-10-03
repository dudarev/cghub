.. about css/js files handling

Compiling CSS and JS
====================

LESS is used to maintain stylesheets.
Client side LESS compilator is used in developement environment.

Some requirements should be satisfied to compile static files from LESS
to CSS and Javascript minification for production environment.

Used 0.10.20 version of nodejs and grunt-cli v0.1.9.

Installation
------------

Remove all versions if exists:

.. code-block:: bash

    sudo apt-get purge nodejs
    sudo rm /usr/local/bin/grunt
    sudo rm /usr/local/bin/grunt-less
    rm node_modules

Install nodejs and grunt:

.. code-block:: bash

    sudo add-apt-repository ppa:chris-lea/node.js
    sudo apt-get update
    sudo apt-get install nodejs
    sudo npm install grunt-cli -g

Install necessary modules:

.. code-block:: bash

    npm install grunt
    npm install grunt-contrib-uglify
    npm install grunt-recess
    mv node_modules cghub/

Usage
-----

To compile from LESS to CSS use ``less`` target:

.. code-block:: bash

    make less

To minify js use ``minjs`` target:

.. code-block:: bash

    make minjs
