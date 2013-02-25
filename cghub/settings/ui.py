"""
TABLE_COLUMNS

Format:
(
(column_name, default_state),
...
)

Available column_names : 'Assembly', 'Barcode', 'Center', 'Center Name',
'Disease', 'Disease Name', 'Experiment Type', 'Files Size',
'Last modified', 'Run Type', 'Sample Accession', 'Sample Type',
'Sample Type Name', 'State', 'Study', 'Upload time', 'UUID'.

Available default_states: 'visible', 'hidden'.
"""

TABLE_COLUMNS = (
    ('UUID', 'visible'),
    ('Study', 'visible'),
    ('Disease', 'visible'),
    ('Disease Name', 'visible'),
    ('Run Type', 'visible'),
    ('Assembly', 'visible'),
    ('Center', 'visible'),
    ('Center Name', 'visible'),
    ('Experiment Type', 'visible'),
    ('Upload time', 'visible'),
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
    'Upload time',
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
    'Library strategy',
    'Sample Accession',
    'Files Size',
)

COLUMN_HELP_HINTS = {
    'UUID': 'Help text for UUID, and this is <a href="#">link</a>, click to view help page!',
    'Study': 'Help text for Study, and this is <a href="#">link</a>, click to view help page!',
}

DEFAULT_PAGINATOR_LIMIT = 10
