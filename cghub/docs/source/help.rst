Help
=================

Help hints for table columns
----------------------------

Text for help hints for every table column can be specified in project settings.

``settings/ui.py``:

.. code-block:: python

    # ui.py

    COLUMN_HELP_HINTS = {
        'UUID': 'Help hint for UUID, and this is <a href="#">link</a>, click to view help page!',
        'State': 'Some help text',
        ...
