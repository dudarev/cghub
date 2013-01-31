"""
TABLE_COLUMNS

Format:
(
(column_name, default_state),
...
)

Available column_names : 'Barcode', 'Center', 'Center Name', 'Disease', 
'Disease Name', 'Experiment Type', 'Files Size', 'Last modified',
'Reference genome', 'Run Type', 'Sample Accession', 'Sample Type',
'Sample Type Name', 'State', 'Study', 'Upload time', 'UUID'.

Available default_states: 'visible', 'hidden'.
"""

TABLE_COLUMNS = (
    ('UUID', 'visible'),
    ('Study', 'visible'),
    ('Disease', 'visible'),
    ('Disease Name', 'visible'),
    ('Run Type', 'visible'),
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
    ('Reference genome', 'visible'),
)

DEFAULT_PAGINATOR_LIMIT = 10
