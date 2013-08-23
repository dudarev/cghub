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
    'Checksum': 'checksum',
    'Disease': 'disease_abbr',
    'Disease Name': 'disease_abbr',
    'Experiment Type': 'analyte_code',
    'Filename': 'filename',
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
for name, attribute in COLUMN_NAMES.iteritems():
    if attribute not in ATTRIBUTES:
        ATTRIBUTES.append(attribute)

SORT_BY_ATTRIBUTES = (
    'analysis_id',
    'analyte_code',
    'center_name',
    'disease_abbr',
    'last_modified',
    'legacy_sample_id',
    'library_strategy',
    'platform',
    'refassem_short_name',
    'sample_accession',
    'sample_type',
    'state',
    'study',
    'upload_date',
)

# present only in RequestFull
ADDITIONAL_ATTRIBUTES = (
    'aliquot_id',
    'participant_id',
    'sample_id',
    'tss_id',
)
