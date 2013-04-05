"""
TABLE_COLUMNS
-------------

Format:

::

    (
        (column_name, default_state),
        ...
    )

Available column_names : 'Assembly', 'Barcode', 'Center', 'Center Name',
'Disease', 'Disease Name', 'Experiment Type', 'Files Size',
'Last modified', 'Library Type', 'Sample Accession', 'Sample Type',
'Sample Type Name', 'State', 'Study', 'Uploaded', 'Analysis Id'.

Available default_states: 'visible', 'hidden'.

VALUE_RESOLVERS
---------------

Some column values can has an absurd names.
This variable used to map them to something a human would understand.

Format:
dict <Column name>:<function>

function obtains value and should return new value, for example:

::

    def study_resolver(val):
        if val.find('Other_Sequencing_Multiisolate') != -1:
            return 'CCLE'
        return val

    VALUE_RESOLVERS = {
        'Study': study_resolver,
    }
"""
COLUMNS = {
    'Analysis Id': {
        'width': 220, 'attr': 'analysis_id', 'align': 'left',
        },
    'Assembly': {
        'width': 120, 'attr': 'refassem_short_name', 'align': 'left',
        },
    'Barcode': {
        'width': 235, 'attr': 'legacy_sample_id', 'align': 'left',
        },
    'Center': {
        'width': 100, 'attr': 'center_name', 'align': 'left',
        },
    'Center Name': {
        'width': 100, 'attr': 'center_name', 'align': 'left',
        },
    'Disease': {
        'width': 65, 'attr': 'disease_abbr', 'align': 'left',
        },
    'Disease Name': {
        'width': 200, 'attr': 'disease_abbr', 'align': 'left',
        },
    'Experiment Type': {
        'width': 95, 'attr': 'analyte_code', 'align': 'left',
        },
    'Files Size': {
        'width': 75, 'attr': 'files_size', 'align': 'right',
        },
    'Library Type': {
        'width': 100, 'attr': 'library_strategy', 'align': 'left',
        },
    'Last modified': {
        'width': 80, 'attr': 'last_modified', 'align': 'left',
        },
    'Sample Accession': {
        'width': 100, 'attr': 'sample_accession', 'align': 'left',
        },
    'Sample Type': {
        'width': 75, 'attr': 'sample_type', 'align': 'left',
        },
    'Sample Type Name': {
        'width': 150, 'attr': 'sample_type', 'align': 'left',
        },
    'State': {
        'width': 70, 'attr': 'state', 'align': 'left',
        },
    'Study': {
        'width': 100, 'attr': 'study', 'align': 'left',
        },
    'Uploaded': {
        'width': 80, 'attr': 'upload_date', 'align': 'left',
        },
    }


TABLE_COLUMNS = (
    ('Analysis Id', 'visible'),
    ('Study', 'visible'),
    ('Disease', 'visible'),
    ('Disease Name', 'visible'),
    ('Library Type', 'visible'),
    ('Assembly', 'visible'),
    ('Center', 'visible'),
    ('Center Name', 'visible'),
    ('Experiment Type', 'visible'),
    ('Uploaded', 'visible'),
    ('Last modified', 'visible'),
    ('Sample Type', 'visible'),
    ('Sample Type Name', 'visible'),
    ('State', 'visible'),
    ('Barcode', 'visible'),
    ('Sample Accession', 'visible'),
    ('Files Size', 'visible'),
)

DETAILS_FIELDS = (
    'State',
    'Last modified',
    'Uploaded',
    'Published time',
    'Center',
    'Center Name',
    'Experiment Type',
    'Study',
    'Aliquot id',
    'Legasy sample id',
    'Disease abbr',
    'Disease Name',
    'Assembly',
    'TSS id',
    'Participant id',
    'Sample id',
    'Sample Type',
    'Sample Type Name',
    'Library Type',
    'Sample Accession',
    'Files Size',
)

def study_resolver(val):
    if val.find('Other_Sequencing_Multiisolate') != -1:
        return 'CCLE'
    return val

VALUE_RESOLVERS = {
    'Study': study_resolver,
}

DEFAULT_PAGINATOR_LIMIT = 10

DEFAULT_FILTERS = {
    'state': ('live',),
    'upload_date': '[NOW-7DAY TO NOW]',
}
