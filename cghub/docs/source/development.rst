.. About development

Development
============================================

-------------------------------
Setting up and running the app
-------------------------------

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
    make migrate

    # in another terminal from `cghub` directory
    make run

-----------------------
Filters customizing
-----------------------

Filters list can be edited in ``cghub/settings/filters.py``:

.. code-block:: python

    ALL_FILTERS = OrderedDict([
    ('study', {
        'title': "By Study",
        'filters': OrderedDict([
            ('TCGA', 'phs000178'),
            ('TCGA Benchmark', 'TCGA_MUT_BENCHMARK_4'),
        ]),
        "selectOptions": True,
        "searchForNewOptions": False,
    }),
    ('center_name', {
        'title': 'By Center',
        ...

Filters supports hierarchical structures:

.. code-block:: python

    ('refassem_short_name', {
        'title': 'By Assembly',
        'filters': OrderedDict([
            ('NCBI36/HG18', OrderedDict([
                ('HG18', 'HG18'),
                ('HG18_Broad_variant', 'HG18_Broad_variant'),
                ('NCBI36_BCCAGSC_variant', 'NCBI36_BCCAGSC_variant'),
                ('NCBI36_BCM_variant', 'NCBI36_BCM_variant'),
                ('NCBI36_WUGSC_variant', 'NCBI36_WUGSC_variant'),
                ('NCBI-human-build36', 'NCBI-human-build36'),
            ])),
            ('NCBI37/HG19', OrderedDict([
                ('HG19', 'HG19'),
                ('HG19_Broad_variant', 'HG19_Broad_variant'),
            ])),
            ('GRCh37-lite-+-HPV_Redux-build', 'GRCh37-lite-+-HPV_Redux-build'),
            ('GRCh37-lite', 'GRCh37-lite'),
            ('GRCh37', 'GRCh37'),
            ('GRCh37_BI_Variant', 'GRCh37_BI_Variant'),
        ]),
        "selectOptions": False,
    })

In case of refassem_short_name, study and dissease_abbr, complex queries with "OR" are allowed:

.. code-block:: python

    ('refassem_short_name', {
        'filters': OrderedDict([
            ('NBCI36* OR HG18*', 'NBCI36/HG18'),
            ('GRCh37* OR HG19*', 'GRCh37/HG19'),
        ]),
        'title': 'By Assembly',
    }),

If 'selectOptions' is True or unspecified, apply the select options algorithm to this filter.
If 'searchForNewOptions' is True, will be scanned all options and displayed missing ones (False is default value).

----------------------------
Filters list shortening
----------------------------

There are many possible options for filters in the sidebar. Not all of them are used by CGHub. To reduce the list a management command ``selectfilters`` is written. It should be used as following:

.. code-block:: bash

    $ python manage.py selectfilters

Can be used verbosity option.
Setting the verbose level to 0 would cause only error message and the warnings about need to add new filters be printed. If there are no problems, selectfilters would be completely silent:

.. code-block:: bash

    $ python manage.py selectfilters --verbosity 0

Command output:

.. code-block:: bash

    Processing study filter
    Processing disease_abbr filter
    ! New option disease_abbr:TEST. Please add this option to filters.py
    ! New option disease_abbr:provolone. Please add this option to filters.py
    Processing sample_type filter
    Processing analyte_code filter
    Processing library_strategy filter
    Processing center_name filter
    Processing platform filter
    Processing refassem_short_name filter
    Processing upload_date filter
    Processing last_modified filter

To add `provolone` name to filters, You should add this filter to cghub/settings/filters.py and reexecute ``selectfilters`` command.

Filters list can be accessed from Filters class from ``filters_storage.py``:

.. code-block:: python

    from cghub.apps.core.filters_storage import Filters


    print Filters.get_all_filters() # will show dict similar to ALL_FILTERS from cghub/settings.filters.py
    print Filters.get_date_filters_html_ids() # will show dict similar to DATE_FILTERS_HTML_IDS from cghub/settings/filters.py

While testing, Filters class obtains data from filters_storage.json.test.
Otherwise it tries to obtain data from filters_storage.json. If this file was not found, Filters class tries to obtain data from filters_storage.json.default.

Filters class loads filters from file only once.
As exception it reloads filters if filters_storage.json was updated (modification_time was changed).

---------------------------
Removing sessions and carts
---------------------------

`clean_sessions` management command allows to remove Sessions,
Carts and Analysises from database at once.

.. code-block:: bash

    python manage.py clean_sessions

--------
Messages
--------

It is possible to add messages to show them to user.
There are two ways to add message:

    - add it to session (using `cghub.apps.core.utils.add_message`)
    - add message by adding notifications variable to response context

Adding messages:

.. code-block:: python

    from cghub.apps.core.utils import add_message


    def myview(request):
        add_message(request=request, level='error', content='Some error!')

This message will be visible on all pages until it will be slosed by user.

Message can be removed by its id:

.. code-block:: python

    from cghub.apps.core.utils import add_message, remove_message


    def myview(request):
        message_id = add_message(request=request, level='error', content='Some error!')
        ...
        remove_message(request, message_id)

Message can be deleted right after it will be shown:

.. code-block:: python

    from cghub.apps.core.utils import add_message, remove_message


    def myview(request):
        message_id = add_message(
                request=request, level='error',
                content='Some error!', once=True)

And this message will be shown only once:

.. code-block:: python

    def myview(request):
        context = {}
        context['notifications'] = [{
            'level': 'error',
            'content': 'Some error!'
        }]
        response = render('simetemplate.html', context)

-------------------------
Database and transcations
-------------------------

Seems like only InnoDB supports transactions.

DATABASES settings should contains:

.. code-block:: python

DATABASES = {
    'default': {
        ...
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            },
        }
}

Transactions used to commit all changes at once or rollback all changes when adding/removing items to cart:

.. code-block:: python

    from django.db import transaction


    with transaction.commit_on_success():
        cart = Cart(request.session)
        for analysis_id in form.cleaned_data['ids']:
            cart.remove(analysis_id)
        cart.update_stats()
