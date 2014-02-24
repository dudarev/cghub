"""
HELP_HINTS
keys have to be like this:
'Analysis Id', 'Study', 'Study:TCGA', 'Diasease Name:Lung adenocarcinoma', ...
"""

# TCGA descriptions should match those in codeTablesReport when possible:
#   https://tcga-data.nci.nih.gov/datareports/codeTablesReport.htm
# filter descriptions should be kept in sync with cghub/apps/core/filters_storage_full.py


HELP_HINTS = {
    ##
    # Filters headers and buttons
    ##
    'common:filters-bar': 'Filter by metadata attributes',
    'filter:Study': 'Filter by research study that generated the data set',
    'filter:Disease': 'Filter by disease',
    'filter:Sample Type': 'Filer by the type of the biological sample that was sequences',
    'filter:Library Type': 'Filter by the type of library protocol',
    'filter:Assembly': 'Filter by reference genome assembly',
    'filter:Center': 'Filter by submitting center',
    'filter:Analyte Type': 'Filter by Molecular analyte',
    'filter:Upload Time': 'Filter by date the data set was uploaded',
    'filter:Modification Time': 'Filter by date the metadata was last modified',
    'filter:State': 'Filter by current state of the data at CGHub',
    'filter:Platform': 'Filter by sequencing platform',
    'common:remember-filters' : 'Remember the filter settings when revisiting the Data Browser',
    'common:filters-reset-button': 'Reset the filters and search text to their default state',
    'common:filters-apply-button': 'Run a search with the specified filters',

    ##
    # Column descriptions
    ##
    'Study': 'Research study that generated the data set',
    'Disease': 'Disease abbreviation',
    'Disease Name': 'Disease name',
    'Library Type': 'Library protocol',
    'Assembly': 'Reference genome assembly',
    'Center': 'Submitting center abbreviation',
    'Center Name': 'Submitting center name',
    'Analyte Type': 'Molecular analyte that was sequenced',
    'Uploaded': 'Date the data set was uploaded',
    'Published': 'Date the data set was available for download',
    'Modified': 'Date the metadata was last modified',
    'Sample Type': 'Type of the biological sample that was sequenced',
    'Sample Type Name': 'Description of the biological sample that was sequenced',
    'State': 'Current state of the data at CGHub',
    'Barcode': 'Aliquot barcode. <a href="https://wiki.nci.nih.gov/display/TCGA/Working+with+TCGA+Data" target="_blank">More information on TCGA barcodes</a>.',
    'Sample Accession': 'NCBI sample accession when available',
    'Filename': 'Name of the primary data file',
    'Files Size': 'Size of the primary data file (GB for gigabytes, MB for megabytes)',
    'Checksum': 'MD5 checksum of the primary data file',
    'Platform': 'Sequencing platform abbreviation',
    'Platform Name': 'Sequencing platform',
    'Analysis Id': 'CGHub identifier of the data set (UUID)',
    'Participant Id': 'Participant identifier (UUID)',
    'Sample Id': 'Sample identifier (UUID)',
    'Aliquot Id': 'Aliquot identifier (UUID)',
    'TSS Id': 'Tissue source site identifier code',

    ##
    # Studies
    ##
    'Study:TCGA': 'The Cancer Genome Atlas',
    'Study:CCLE': 'Cancer Cell Line Encyclopedia',
    'Study:TARGET': 'Therapeutically Applicable Research to Generate Effective Treatments',
    'Study:TARGET (ALL I)':  'TARGET: Acute Lymphoblastic Leukemia (ALL) Phase I Pilot',
    'Study:TARGET (ALL II)': 'TARGET: Acute Lymphoblastic Leukemia (ALL) Phase II',
    'Study:TARGET (AML)':    'TARGET: Acute Myeloid Leukemia (AML)',
    'Study:TARGET (CCSK)':   'TARGET: Kidney - Clear Cell Sarcoma of the Kidney (CCSK)',
    'Study:TARGET (NBL)':    'TARGET: Neuroblastoma (NBL)',
    'Study:TARGET (OS)':     'TARGET: Osteosarcoma (OS)',
    'Study:TARGET (PPTP)':   'TARGET: PPTP Cell Lines',
    'Study:TARGET (WT)':     'TARGET: Kidney - Wilms Tumor (WT)',
    'Study:CGCI':            'CGCI',
    'Study:TCGA Benchmark': 'TCGA Mutation Calling Benchmark 4 (artificial data)',

    ##
    # Center abbreviations [warning: DCC center short names are not the same as the NCBI names and not used]
    # This information is also maintained in ui.py
    ##
    'Center:BCM': 'Baylor College of Medicine',
    'Center:BCCAGSC': 'Canada\'s Michael Smith Genome Sciences Centre',
    'Center:BI': 'Broad Institute of MIT and Harvard',
    'Center:HMS-RK': 'Harvard Medical School',
    'Center:UNC-LCCC': 'University of North Carolina',
    'Center:USC-JHU': 'University of Southern California / Johns Hopkins',
    'Center:WUGSC': 'Washington University School of Medicine',

    ##
    # Disease
    # FIXME: this is duplicated in filters_storage_full.py
    ##
    "Disease:ACC":  "Adrenocortical carcinoma",
    "Disease:BLCA": "Bladder Urothelial Carcinoma",
    "Disease:BRCA": "Breast invasive carcinoma",
    "Disease:CESC": "Cervical squamous cell carcinoma and endocervical adenocarcinoma",
    "Disease:CNTL": "Controls",
    "Disease:COAD": "Colon adenocarcinoma",
    "Disease:DLBC": "Lymphoid Neoplasm Diffuse Large B-cell Lymphoma",
    "Disease:ESCA": "Esophageal carcinoma",
    "Disease:GBM":  "Glioblastoma multiforme",
    "Disease:HNSC": "Head and Neck squamous cell carcinoma",
    "Disease:KICH": "Kidney Chromophobe",
    "Disease:KIRC": "Kidney renal clear cell carcinoma",
    "Disease:KIRP": "Kidney renal papillary cell carcinoma",
    "Disease:LAML": "Acute Myeloid Leukemia",
    "Disease:AML": "Acute Myeloid Leukemia",
    "Disease:LCLL": "Chronic Lymphocytic Leukemia",
    "Disease:LCML": "Chronic Myelogenous Leukemia",
    "Disease:LGG":  "Brain Lower Grade Glioma",
    "Disease:LIHC": "Liver hepatocellular carcinoma",
    "Disease:LUAD": "Lung adenocarcinoma",
    "Disease:LUSC": "Lung squamous cell carcinoma",
    "Disease:MESO": "Mesothelioma",
    "Disease:MISC": "Miscellaneous",
    "Disease:MM":   "Multiple Myeloma Plasma cell leukemia",
    "Disease:OV":   "Ovarian serous cystadenocarcinoma",
    "Disease:PAAD": "Pancreatic adenocarcinoma",
    "Disease:PCPG": "Pheochromocytoma and Paraganglioma",
    "Disease:PRAD": "Prostate adenocarcinoma",
    "Disease:READ": "Rectum adenocarcinoma",
    "Disease:SARC": "Sarcoma",
    "Disease:SKCM": "Skin Cutaneous Melanoma",
    "Disease:STAD": "Stomach adenocarcinoma",
    "Disease:THCA": "Thyroid carcinoma",
    "Disease:UCEC": "Uterine Corpus Endometrioid Carcinoma",
    "Disease:UCS":  "Uterine Carcinosarcoma",
    "Disease:UVM":  "Uveal Melanoma",
    # keys for filters sidebar and applied filters
    "Disease:Acute Lymphoblastic Leukemia": "Acute Lymphoblastic Leukemia",
    "Disease:Acute Myeloid Leukemia": "Acute Myeloid Leukemia",
    "Disease:Adrenocortical carcinoma": "Adrenocortical carcinoma",
    "Disease:Bladder Urothelial Carcinoma": "Bladder Urothelial Carcinoma",
    "Disease:Brain Lower Grade Glioma": "Brain Lower Grade Glioma",
    "Disease:Breast invasive carcinoma": "Breast invasive carcinoma",
    "Disease:Cervical squamous cell carcinoma and endocervical adenocarcinoma": "Cervical squamous cell carcinoma and endocervical adenocarcinoma",
    "Disease:Chronic Lymphocytic Leukemia": "Chronic Lymphocytic Leukemia",
    "Disease:Chronic Myelogenous Leukemia": "Chronic Myelogenous Leukemia",
    "Disease:Clear Cell Sarcoma of the Kidney": "Clear Cell Sarcoma of the Kidney",
    "Disease:Colon adenocarcinoma": "Colon adenocarcinoma",
    "Disease:Controls": "Controls",
    "Disease:Esophageal carcinoma": "Esophageal carcinoma",
    "Disease:Glioblastoma multiforme": "Glioblastoma multiforme",
    "Disease:Head and Neck squamous cell carcinoma": "Head and Neck squamous cell carcinoma",
    "Disease:Kidney Chromophobe": "Kidney Chromophobe",
    "Disease:Kidney renal clear cell carcinoma": "Kidney renal clear cell carcinoma",
    "Disease:Kidney renal papillary cell carcinoma": "Kidney renal papillary cell carcinoma",
    "Disease:Liver hepatocellular carcinoma": "Liver hepatocellular carcinoma",
    "Disease:Lung adenocarcinoma": "Lung adenocarcinoma",
    "Disease:Lung squamous cell carcinoma": "Lung squamous cell carcinoma",
    "Disease:Lymphoid Neoplasm Diffuse Large B-cell Lymphoma": "Lymphoid Neoplasm Diffuse Large B-cell Lymphoma",
    "Disease:Mesothelioma": "Mesothelioma",
    "Disease:Miscellaneous": "Miscellaneous",
    "Disease:Multiple Myeloma Plasma cell leukemia": "Multiple Myeloma Plasma cell leukemia",
    "Disease:Neuroblastoma": "Neuroblastoma",
    "Disease:Osteosarcoma": "Osteosarcoma",
    "Disease:Ovarian serous cystadenocarcinoma": "Ovarian serous cystadenocarcinoma",
    "Disease:Pancreatic adenocarcinoma": "Pancreatic adenocarcinoma",
    "Disease:Pheochromocytoma and Paraganglioma": "Pheochromocytoma and Paraganglioma",
    "Disease:Prostate adenocarcinoma": "Prostate adenocarcinoma",
    "Disease:Rectum adenocarcinoma": "Rectum adenocarcinoma",
    "Disease:Sarcoma": "Sarcoma",
    "Disease:Skin Cutaneous Melanoma": "Skin Cutaneous Melanoma",
    "Disease:Stomach adenocarcinoma": "Stomach adenocarcinoma",
    "Disease:Thyroid carcinoma": "Thyroid carcinoma",
    "Disease:Uterine Carcinosarcoma": "Uterine Carcinosarcoma",
    "Disease:Uterine Corpus Endometrioid Carcinoma": "Uterine Corpus Endometrioid Carcinoma",
    "Disease:Uveal Melanoma": "Uveal Melanoma",
    "Disease:Wilms Tumor": "Wilms Tumor",

    ##
    # Library Type
    ##
    'Library Type:Bisulfite-Seq': 'Bisulfite Sequencing',
    'Library Type:RNA-Seq': 'Transcriptome Sequencing',
    'Library Type:VALIDATION': 'Re-sequencing to verify mutation calls',
    'Library Type:WGS': 'Whole Genome Sequencing',
    'Library Type:WXS': 'Whole Exome Sequencing',
    'Library Type:miRNA-Seq': 'micro-RNA Sequencing ',
    'Library Type:OTHER': 'Uncategorized library strategy',

    ##
    # By Analyte Type
    ##
    'Analyte Type:DNA': 'DNA analyte',
    'Analyte Type:GenomePlex': 'Whole Genome Amplification (WGA) produced using GenomePlex (Rubicon) DNA',
    'Analyte Type:miRNA': 'mirVana RNA (Allprep DNA) produced by hybrid protocol',
    'Analyte Type:RNA': 'RNA analyte',
    'Analyte Type:Total RNA': 'Total RNA analyte',
    'Analyte Type:WGA': 'Whole Genome Amplification (WGA) produced using Repli-G (Qiagen) DNA',
    'Analyte Type:WGA X': 'Whole Genome Amplification (WGA) produced using Repli-G X (Qiagen) DNA (2nd Reaction)',

    ##
    # Assembly - These are linked to the help/assemblies.html page and must be
    # kept in sync.
    ##
    'Assembly:NCBI36/HG18 based': 'All assembly variants based on NCBI36/HG18',
    'Assembly:GRCh37/HG19 based': 'All assembly variants based on GRCh37/HG19',

    'Assembly:NCBI-human-build36': 'NCBI human reference assembly build 36. <a href="/help/assemblies#NCBI-human-build36" target="_blank">More information on assemblies</a>.',
    'Assembly:NCBI36_BCCAGSC_variant': 'A variant of the full NCBI36 human genome assembly used by the British Columbia Cancer Agency Genome Sciences Centre (BCCAGSC). <a href="/help/assemblies#NCBI36_BCCAGSC_variant" target="_blank">More information</a>.',
    'Assembly:NCBI36_BCM_variant': 'A variant of the full NCBI36 human genome assembly used by Baylor College of Medicine Human Genome Sequencing Center. <a href="/help/assemblies#NCBI36_BCM_variant" target="_blank">More information</a>.',
    'Assembly:NCBI36_WUGSC_variant': 'A variant of the full NCBI36 human genome assembly used by Washington University Genome Sequencing Center (WUGSC). <a href="/help/assemblies#NCBI36_WUGSC_variant" target="_blank">More information</a>.',
    'Assembly:HG18': 'UCSC variant of NCBI human reference assembly build 36. <a href="/help/assemblies#HG18" target="_blank">More information</a>.',
    'Assembly:HG18_Broad_variant': 'A variant of the NCBI36 human genome assembly used by the Broad Institute. <a href="/help/assemblies#HG18_Broad_variant" target="_blank">More information</a>.',

    'Assembly:GRCh37': 'GRCh37 human genome assembly. <a href="/help/assemblies#GRCh37" target="_blank">More information</a>.',
    'Assembly:GRCh37-lite-+-HPV_Redux-build': 'A variant of the GRCh37-lite human genome assembly used by the Broad Institute that includes the HPV viral genome. <a href="/help/assemblies#GRCh37-lite_HPV_Redux-build" target="_blank">More information</a>.',
    'Assembly:GRCh37-lite': 'A subset of the full GRCh37 human genome assembly plus the human mitochondrial genome reference sequence. <a href="/help/assemblies#GRCh37-lite" target="_blank">More information</a>.',
    'Assembly:GRCh37_BI_Variant': 'A variant of the GRCh37-lite human genome assembly used by the Broad Institute. <a href="/help/assemblies#GRCh37_BI_Variant" target="_blank">More information</a>.',
    'Assembly:HG19': 'UCSC variant of GRCh37 human genome assembly. <a href="/help/assemblies#HG19" target="_blank">More information</a>.',
    'Assembly:HG19_Broad_variant': 'A variant of the GRCh37 human genome assembly used by the Broad Institute. <a href="/help/assemblies#HG19_Broad_variant" target="_blank">More information</a>.',
    'Assembly:unaligned': 'FASTQ file of reads that have not been aligned to an assembly. <a href="/help/assemblies#unaligned" target="_blank">More information</a>.',

    ##
    # State
    ##
    'State:Bad data': 'Data files failed the checksum process after being uploaded to CGHub',
    'State:Live': 'Data is available for downloaded',
    'State:Submitted': 'Metadata has passed validation, waiting on uploading of data file(s)',
    'State:Uploading': 'Uploading the data file(s) is in progress',
    'State:Validating sample': 'Additional sample metadata is collected from the DCC',
    'State:Augmenting data': 'Supplementary data files are being added to the data set, temporarily unavailable for download',
    'State:Suppressed': 'Data has been suppressed',
    'State:Redacted': 'Sample has been redacted',

    ##
    # Sample type
    ##
    'Sample Type:TP': 'Primary Solid Tumor',
    'Sample Type:TR': 'Recurrent Solid Tumor',
    'Sample Type:TB': 'Primary Blood Derived Cancer - Peripheral Blood',
    'Sample Type:TRBM': 'Recurrent Blood Derived Cancer - Bone Marrow',
    'Sample Type:TAP': 'Additional - New Primary',
    'Sample Type:TM': 'Metastatic',
    'Sample Type:TAM': 'Additional Metastatic',
    'Sample Type:THOC': 'Human Tumor Original Cells',
    'Sample Type:TBM': 'Primary Blood Derived Cancer - Bone Marrow',
    'Sample Type:pnat': 'Post neo-adjuvant therapy',
    'Sample Type:NB': 'Blood Derived Normal',
    'Sample Type:NT': 'Solid Tissue Normal',
    'Sample Type:NBC': 'Buccal Cell Normal',
    'Sample Type:NEBV': 'EBV Immortalized Normal',
    'Sample Type:NBM': 'Bone Marrow Normal',
    'Sample Type:fn': 'Fibroblast Normal',
    'Sample Type:CELLC': 'Control Analyte',
    'Sample Type:TRB': 'Recurrent Blood Derived Cancer - Peripheral Blood',
    'Sample Type:tbpt': 'Post treatment Blood Cancer Bone Marrow',
    'Sample Type:bmpt': 'Post treatment Blood Cancer Blood',
    'Sample Type:CELL': 'Cell Lines',
    'Sample Type:XP': 'Primary Xenograft Tissue',
    'Sample Type:XCL': 'Cell Line Derived Xenograft Tissue',
    'Sample Type:gran': 'Granulocytes',

    ##
    # Platform
    ##
    'Platform:LS454': '454',
    'Platform:ILLUMINA': 'Illumina',
    'Platform:HELICOS': 'Helicos',
    'Platform:ABI_SOLID': 'ABI Solid',
    'Platform:COMPLETE_GENOMICS': 'Complete Genomics',
    'Platform:PACBIO_SMRT': 'Pacific Biosciences',
    'Platform:ION_TORRENT': 'Ion Torrent',
    'Platform:CAPILLARY': 'Capillary electrophoresis',

    ##
    # Results panel
    ##
    'common:columns-menu': 'Control which columns are displayed',
    'common:results-add-to-cart-button': 'Add data sets selected in check boxes to the cart',
    'common:results-add-all-to-cart-button': 'Add all search results to the cart',

    ##
    # Top bar
    ##
    'common:ucsc-home-page-link': 'UCSC home page',
    'common:browser-link': 'Main browser page',
    'common:cart-link': 'Management page for items you have selected',
    'common:help-link': 'Information on how to use the data browser',
    'common:search-box': 'Text search of metadata. <a href="/help/overview#text-search" target="_blank">More Information</a>.',
    'common:cghub-home-page-link': 'CGHub home page',

    ##
    # Cart
    ##
    'common:cart-remove': 'Removes the selected items from the cart, one at a time or multiple items at once',
    'common:cart-clear': 'Removes all items from the cart',
    'common:cart-download-manifest': 'Create a manifest file (manifest.xml) that can be passed to GeneTorrent to download all the selected items in your cart',
    'common:cart-download-urls': 'Create a file of analysis data URLs, one per line (urls.txt).  This can be easily parsed for use in partitioning downloads.',
    'common:cart-download-metadata': 'Create a file of the SRA metadata for all items in the cart (metadata.xml).',
    'common:cart-download-summary': 'Creates a summary of the basic metadata associated with each item in a tab-separated-value formatted file (summary.tsv)',

    ##
    # metadata viewer
    ##
    'common:details-show-xml': 'View the full metadata in XML format',
    'common:details-xml-download': 'Download a complete XML file that can be displayed in your browser',
    'common:details-add-to-cart': 'Add item to cart',
}
