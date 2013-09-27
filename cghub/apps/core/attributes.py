"""
This file stores list of attributes and them relations to column names
"""

DATE_ATTRIBUTES = (
    'last_modified',
    'upload_date',
    'published_date'
)

COLUMN_NAMES = {
    'Aliquot Id': 'aliquot_id',
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
    'Participant Id': 'participant_id',
    'Published': 'published_date',
    'Platform': 'platform',
    'Platform Name': 'platform',
    'Preservation Method': 'preservation_method',
    'Reason': 'reason',
    'Sample Accession': 'sample_accession',
    'Sample Id': 'sample_id',
    'Sample Type': 'sample_type',
    'Sample Type Name': 'sample_type',
    'State': 'state',
    'Study': 'study',
    'TSS Id': 'tss_id',
    'Uploaded': 'upload_date',
}

ATTRIBUTES = []
for name, attribute in COLUMN_NAMES.iteritems():
    if attribute not in ATTRIBUTES:
        ATTRIBUTES.append(attribute)

SORT_BY_ATTRIBUTES = [
    'aliquot_id',
    'analysis_id',
    'analyte_code',
    'center_name',
    'disease_abbr',
    'last_modified',
    'legacy_sample_id',
    'library_strategy',
    'published_date',
    'participant_id',
    'platform',
    'refassem_short_name',
    'sample_accession',
    'sample_id',
    'sample_type',
    'state',
    'study',
    'tss_id',
    'upload_date',
]

CART_SORT_ATTRIBUTES = SORT_BY_ATTRIBUTES + [
    'checksum',
    'filename',
    'files_size',
]
