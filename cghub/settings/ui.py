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
    ('State', 'visible'),
    ('Last modified', 'visible'),
    ('Upload time', 'visible'),
    ('Published time', 'visible'),
    ('Center', 'visible'),
    ('Center Name', 'visible'),
    ('Experiment Type', 'visible'),
    ('Study', 'visible'),
    ('Aliquot id', 'visible'),
    ('Legasy sample id', 'visible'),
    ('Disease abbr', 'visible'),
    ('Disease Name', 'visible'),
    ('Assembly', 'visible'),
    ('TSS id', 'visible'),
    ('Participant id', 'visible'),
    ('Sample id', 'visible'),
    ('Sample Type', 'visible'),
    ('Sample Type Name', 'visible'),
    ('Library strategy', 'visible'),
    ('Sample Accession', 'visible'),
    ('Files Size', 'visible'),
)


DEFAULT_PAGINATOR_LIMIT = 10
