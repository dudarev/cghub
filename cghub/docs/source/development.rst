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
