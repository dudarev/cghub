"""
HELP_HINTS
keys have to be like this:
'UUID', 'Study', 'Study:TCGA', 'Diasease Name:Lung adenocarcinoma', ...
"""


HELP_HINTS = {
    # help hints for headers in results table, taken from settings.TABLE_COLUMNS
    'UUID': 'Sample tooltip for column "UUID", and this is <a href="#" class="js-help-link" data-slug="uuid-help">link</a>, click to view help page!',
    'Study': 'Sample tooltip for column "Study"',
    'Disease': 'Sample tooltip for column "Disease"',
    'Disease Name': 'Sample tooltip for column "Disease Name"',
    'Library Type': 'Sample tooltip for column "Library Type"',
    'Assembly': 'Sample tooltip for column "Assembly"',
    'Center': 'Sample tooltip for column "Center"',
    'Center Name': 'Sample tooltip for column "Center Name"',
    'Experiment Type': 'Sample tooltip for column "Experiment Type"',
    'Uploaded': 'Sample tooltip for column "Uploaded"',
    'Last modified': 'Sample tooltip for column "Last modified"',
    'Sample Type': 'Sample tooltip for column "Sample Type"',
    'Sample Type Name': 'Sample tooltip for column "Sample Type Name"',
    'State': 'Sample tooltip for column "State"',
    'Barcode': 'Sample tooltip for column "Barcode"',
    'Sample Accession': 'Sample tooltip for column "Sample Accession"',
    'Files Size': 'Sample tooltip for column "Files Size"',

    # help hints for filter titles (here should be placed all titles from filters_storage_full.py, without "By")
    'filter:Study': 'Sample tooltip for filter "Study"',
    'filter:Center': 'Sample tooltip for filter "Center"',
    'filter:Experiment Type': 'Sample tooltip for filter "Experiment Type"',
    'filter:Upload Time': 'Sample tooltip for filter "Upload Time"',
    'filter:Time Modified': 'Sample tooltip for filter "Time Modified"',
    'filter:Sample Type': 'Sample tooltip for filter "Sample Type"',
    'filter:Library Type': 'Sample tooltip for filter "Library Type"',
    'filter:Assembly': 'Sample tooltip for filter "Assembly"',
    'filter:Disease': 'Sample tooltip for filter "Disease"',
    'filter:State': 'Sample tooltip for filter "State"',

    # help hints for filters in dropdown, selected filters and cells in table
    'Study:TCGA': 'Sample tooltip for "Study/TCGA"',
    'Study:TCGA Benchmark': 'Sample tooltip for "Study/TCGA Benchmark"',
}
