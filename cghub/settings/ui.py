"""
TABLE_COLUMNS
-------------

Format:

::

    (
        (column_name, default_state, text-align),
        ...
    )

Available column_names : 'Assembly', 'Barcode', 'Center', 'Center Name',
'Disease', 'Disease Name', 'Experiment Type', 'Files Size',
'Last modified', 'Library Type', 'Sample Accession', 'Sample Type',
'Sample Type Name', 'State', 'Study', 'Uploaded', 'Analysis Id'.

Available default_states: 'visible', 'hidden'.

Available text-align: 'center', 'justify', 'left', 'right', 'inherit'

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

TABLE_COLUMNS = (
    ('Analysis Id', 'visible', 'left'),
    ('Study', 'visible', 'left'),
    ('Disease', 'visible', 'left'),
    ('Disease Name', 'hidden', 'left'),
    ('Library Type', 'visible', 'left'),
    ('Assembly', 'visible', 'left'),
    ('Center', 'visible', 'left'),
    ('Center Name', 'hidden', 'left'),
    ('Experiment Type', 'hidden', 'left'),
    ('Uploaded', 'hidden', 'left'),
    ('Last modified', 'visible', 'left'),
    ('Sample Type', 'visible', 'left'),
    ('Sample Type Name', 'hidden', 'left'),
    ('State', 'visible', 'left'),
    ('Barcode', 'visible', 'left'),
    ('Sample Accession', 'hidden', 'left'),
    ('Files Size', 'visible', 'right'),
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
