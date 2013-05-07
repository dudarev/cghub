"""
This file stores list of attributes and them relations to column names
"""

DATE_ATTRIBUTES = (
    'last_modified',
    'upload_date',
    'published_date'
)

COLUMN_NAMES = {
    'Analysis Id': 'analysis_id',
    'Assembly':  'refassem_short_name',
    'Barcode': 'legacy_sample_id',
    'Center': 'center_name',
    'Center Name': 'center_name',
    'Disease': 'disease_abbr',
    'Disease Name': 'disease_abbr',
    'Experiment Type': 'analyte_code',
    'Files Size': 'files_size',
    'Library Type': 'library_strategy',
    'Modified': 'last_modified',
    'Platform': 'platform',
    'Platform Name': 'platform',
    'Sample Accession': 'sample_accession',
    'Sample Type': 'sample_type',
    'Sample Type Name': 'sample_type',
    'State': 'state',
    'Study': 'study',
    'Uploaded': 'upload_date',
}

ATTRIBUTES = []
for name in COLUMN_NAMES:
    if COLUMN_NAMES[name] not in ATTRIBUTES:
        ATTRIBUTES.append(COLUMN_NAMES[name])
