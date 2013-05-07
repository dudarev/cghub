"""
COLUMNS
-------

List of columns to display:

::

    TABLE_COLUMNS = (
        'Study',
        'Disease',

Available column_names: 'Assembly', 'Barcode', 'Center', 'Center Name',
'Disease', 'Disease Name', 'Experiment Type', 'Files Size',
'Library Type', 'Modified', 'Platform', 'Platform Name', 'Sample Accession',
'Sample Type', 'Sample Type Name', 'State', 'Study', 'Uploaded', 'Analysis Id'.

Styles of the columns:

::

    COLUMN_STYLES = {
        'Analysis Id': {
            'width': 220, 'align': 'left', 'default_state': 'visible',
        },
        'Assembly': {
            'width': 120, 'align': 'left', 'default_state': 'visible',
        },

If style for column will be not specified, will be used default styles:

::

    {
        'width': 100,
        'align': 'left',
        'default_state': 'visible'
    }

Available align values: center, justify, left, right, inherit.
Available default_state values: 'visible', 'hidden'.

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

COLUMN_STYLES = {
    'Analysis Id': {
        'width': 220, 'align': 'left', 'default_state': 'visible',
        },
    'Assembly': {
        'width': 120, 'align': 'left', 'default_state': 'visible',
        },
    'Barcode': {
        'width': 235, 'align': 'left', 'default_state': 'visible',
        },
    'Center': {
        'width': 100, 'align': 'left', 'default_state': 'visible',
        },
    'Center Name': {
        'width': 100, 'align': 'left', 'default_state': 'hidden',
        },
    'Disease': {
        'width': 65, 'align': 'left', 'default_state': 'visible',
        },
    'Disease Name': {
        'width': 200, 'align': 'left', 'default_state': 'hidden',
        },
    'Experiment Type': {
        'width': 95, 'align': 'left', 'default_state': 'hidden',
        },
    'Files Size': {
        'width': 75, 'align': 'right', 'default_state': 'visible',
        },
    'Library Type': {
        'width': 100, 'align': 'left', 'default_state': 'visible',
        },
    'Modified': {
        'width': 80, 'align': 'left', 'default_state': 'visible',
        },
    'Platform': {
        'width': 100, 'align': 'left', 'default_state': 'visible',
        },
    'Platform Name': {
        'width': 200, 'align': 'left', 'default_state': 'hidden',
        },
    'Sample Accession': {
        'width': 100, 'align': 'left', 'default_state': 'hidden',
        },
    'Sample Type': {
        'width': 75, 'align': 'left', 'default_state': 'visible',
        },
    'Sample Type Name': {
        'width': 150, 'align': 'left', 'default_state': 'hidden',
        },
    'State': {
        'width': 70, 'align': 'left', 'default_state': 'visible',
        },
    'Study': {
        'width': 100, 'align': 'left', 'default_state': 'visible',
        },
    'Uploaded': {
        'width': 80, 'align': 'left', 'default_state': 'hidden',
        },
}


TABLE_COLUMNS = (
    'Study',
    'Barcode',
    'Disease',
    'Disease Name',
    'Sample Type',
    'Sample Type Name',
    'Experiment Type',
    'Library Type',
    'Center',
    'Center Name',
    'Platform',
    'Platform Name',
    'Assembly',
    'Files Size',
    'Analysis Id',
    'Sample Accession',
    'Uploaded',
    'Modified',
    'State',
)

DETAILS_FIELDS = (
    'Study',
    'Barcode',
    'Disease',
    'Disease Name',
    'Sample Type',
    'Sample Type Name',
    'Experiment Type',
    'Library Type',
    'Center',
    'Center Name',
    'Platform',
    'Platform Name',
    'Assembly',
    'Files Size',
    'Analysis Id',
    'Sample Accession',
    'Uploaded',
    'Modified',
    'State',
    'Aliquot id',
    'TSS id',
    'Participant id',
    'Sample id',
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
    'study': ('phs000178','*Other_Sequencing_Multiisolate'),
    'state': ('live',),
}
