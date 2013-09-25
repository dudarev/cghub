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

Filters list can be edited in ``cghub/apps/core/filters_storage_full.py``:

.. code-block:: python

    ALL_FILTERS = OrderedDict([
    ('study', {
        'title': "By Study",
        'filters': OrderedDict([
            ('TCGA', 'phs000178'),
            ('TCGA Benchmark', 'TCGA_MUT_BENCHMARK_4'),
        ])
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
        "selectFilter": False,
    })

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

Can be used verbosity option.
Setting the verbose level to 0 would cause only error message and the warnings about need to add new filters be printed. If there are no problems, selectfilters would be completely silent:

.. code-block:: bash

    $ python manage.py selectfilters --verbosity 0

Command output:

.. code-block:: bash

    Processing study filter
    Processing disease_abbr filter
    ! New option disease_abbr:TEST. Please add this option to filters_storage_full.py
    ! New option disease_abbr:provolone. Please add this option to filters_storage_full.py
    Processing sample_type filter
    Processing analyte_code filter
    Processing library_strategy filter
    Processing center_name filter
    Processing platform filter
    Processing refassem_short_name filter
    Processing upload_date filter
    Processing last_modified filter

To add `provolone` name to filters, You should add this filter to filters_storage_full.py and reexecute ``selectfilters`` command.

Filters list can be accessed from ``filters_storage.py``, where automatically creates ALL_FILTERS variable and populates by data stored in ``filters_storage.json``. If ``filters_storage.json`` will be missed, then ``filters_storage.json.default`` will be used instead.

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

And this message will be shown only once:

.. code-block:: python

    def myview(request):
        context = {}
        context['notifications'] = [{
            'level': 'error',
            'content': 'Some error!'
        }]
        response = render('simetemplate.html', context)
