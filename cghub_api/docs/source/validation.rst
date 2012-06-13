.. 

Validating schemas
============================================

To validate if data from the server corresponds to schema one may use a few validation scripts located at 
``utils/try_lxml_validate`` and ``utils/try_pyxb``.

To get the source clone it from Github:

.. code-block:: bash

    git clone git://github.com/dudarev/cghub.git


Install requirements if needed.

.. code-block:: bash

    cd cghub
    pip install -r requirements.txt

Change to corresponding directories and run the relevant scripts:

.. code-block:: bash

    cd cghub/cghub_api/utils/try_lxml_validate/
    python validate.py

.. code-block:: bash

    cd cghub/cghub_api/utils/try_pyxb/
    python parse.py

Both these files use a test file stored at ``../../tests/test_data/aliquot_id.xml`` and schemas that were pre-downloaded and stored in the repository.

One may get a file with ``cgquery`` command (see :doc:`cgquery` in this documentation). This needs to be done in both ``try_*`` directories (or the file should be copied).

.. code-block:: bash

    cgquery -a "aliquot_id=087484e8-dc3e-461a-be5f-4217b7c39732" -o out.xml

and use

.. code-block:: bash

    python validate.py -f out.xml

or

.. code-block:: bash

    python parse.py -f out.xml
