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
    'filter:Study': 'Filter by research study that the generated the data set',
    'filter:Disease': 'Filter by disease',
    'filter:Sample Type': 'Filer by the type of the biological sample that was sequences',
    'filter:Library Type': 'Filter by the type of library protocol',
    'filter:Assembly': 'Filter by reference genome assembly',
    'filter:Center': 'Filter by submitting center',
    'filter:Experiment Type': 'Filter by Molecular analyte',
    'filter:Upload Time': 'Filter by date the data set was uploaded',
    'filter:Modification Time': 'Filter by date the metadata was last modified',
    'filter:State': 'Filter by current state of the data at CGHub',
    'filter:Platform': 'Filter by sequencing platform',
    'common:filters-reset-button': 'Reset the filters to their default state',
    'common:filters-apply-button': 'Run a search with the specified filters',

    ##
    # Studies
    ##
    'Study:TCGA': 'The Cancer Genome Atlas',
    'Study:CCLE': 'Cancer Cell Line Encyclopedia',
    'Study:TCGA Benchmark': 'TCGA Mutation Calling Benchmark 4',

    ##
    # Center abbreviations [warning: DCC center short names are not the same and not used]
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
    ##
    'Disease:LAML': 'Acute Myeloid Leukemia',
    'Disease:BLCA': 'Bladder Urothelial Carcinoma',
    'Disease:LGG':  'Brain Lower Grade Glioma',
    'Disease:BRCA': 'Breast invasive carcinoma',
    'Disease:CESC': 'Cervical squamous cell carcinoma and endocervical adenocarcinoma',
    'Disease:LCLL': 'Chronic Lymphocytic Leukemia',
    'Disease:COAD': 'Colon adenocarcinoma',
    'Disease:CNTL': 'Controls',
    'Disease:ESCA': 'Esophageal carcinoma',
    'Disease:GBM':  'Glioblastoma multiforme',
    'Disease:HNSC': 'Head and Neck squamous cell carcinoma',
    'Disease:KICH': 'Kidney Chromophobe',
    'Disease:KIRC': 'Kidney renal clear cell carcinoma',
    'Disease:KIRP': 'Kidney renal papillary cell carcinoma',
    'Disease:LIHC': 'Liver hepatocellular carcinoma',
    'Disease:LUAD': 'Lung adenocarcinoma',
    'Disease:LUSC': 'Lung squamous cell carcinoma',
    'Disease:DLBC': 'Lymphoid Neoplasm Diffuse Large B-cell Lymphoma',
    'Disease:OV':   'Ovarian serous cystadenocarcinoma',
    'Disease:PAAD': 'Pancreatic adenocarcinoma',
    'Disease:PRAD': 'Prostate adenocarcinoma',
    'Disease:READ': 'Rectum adenocarcinoma',
    'Disease:SARC': 'Sarcoma',
    'Disease:SKCM': 'Skin Cutaneous Melanoma',
    'Disease:STAD': 'Stomach adenocarcinoma',
    'Disease:THCA': 'Thyroid carcinoma',
    'Disease:UCEC': 'Uterine Corpus Endometrioid Carcinoma',

    ##
    # Column descriptions
    ##
    'Study': 'Research study that the generated the data set',
    'Disease': 'Disease abbreviation',
    'Disease Name': 'Disease name',
    'Library Type': 'Library protocol',
    'Assembly': 'Reference genome assembly',
    'Center': 'Submitting center abbreviation',
    'Center Name': 'Submitting center name',
    'Experiment Type': 'Molecular analyte that was sequenced',
    'Uploaded': 'Date the data set was uploaded',
    'Modified': 'Date the metadata was last modified',
    'Sample Type': 'Type of the biological sample that was sequenced',
    'Sample Type Name': 'Description of the biological sample that was sequenced',
    'State': 'Current state of the data at CGHub',
    'Barcode': 'Aliquot barcode. <a href="https://wiki.nci.nih.gov/display/TCGA/Working+with+TCGA+Data">Click here for a detailed description of TCGA barcode</a>.',
    'Sample Accession': 'NCBI sample accession when available',
    'Files Size': 'Size of the data set (GB for gigabytes, MB for megabytes)',
    'Platform': 'Sequencing platform abbreviation',
    'Platform Name': 'Sequencing platform',

    ##
    # Library Type
    ##
    'Library Type:Bisulfite-Seq': 'Bisulfite Sequencing',
    'Library Type:RNA-Seq': 'Transcriptome Sequencing',
    'Library Type:VALIDATION': 'Re-sequencing to verify mutation calls',
    'Library Type:WGS': 'Whole Genome Sequencing',
    'Library Type:WXS': 'Whole Exeome Sequencing',
    'Library Type:miRNA-Seq': 'micro-RNA Sequencing ',
    'Library Type:OTHER': 'Uncategorized library strategy',

    ##
    # By Experiment Type
    ##
    'Experiment Type:DNA': 'DNA analyte',
    'Experiment Type:GenomePlex': 'Whole Genome Amplification (WGA) produced using GenomePlex (Rubicon) DNA',
    'Experiment Type:miRNA': 'mirVana RNA (Allprep DNA) produced by hybrid protocol',
    'Experiment Type:RNA': 'RNA analyte',
    'Experiment Type:Total RNA': 'Total RNA analyte',
    'Experiment Type:WGA': 'Whole Genome Amplification (WGA) produced using Repli-G (Qiagen) DNA',
    'Experiment Type:WGA X': 'Whole Genome Amplification (WGA) produced using Repli-G X (Qiagen) DNA (2nd Reaction)',

    ##
    # Assembly - These are linked to the help/assemblies.html page and must be
    # kept in sync.
    ##
    'Assembly:NCBI36/HG18 based': 'All assembly variants based on NCBI36/HG18',
    'Assembly:GRCh37/HG19 based': 'All assembly variants based on GRCh37/HG19',

    'Assembly:NCBI-human-build36': 'NCBI human reference assembly build 36. <a href="../help/assemblies#NCBI-human-build36">Click here for more detailed information</a>.',
    'Assembly:NCBI36_BCCAGSC_variant': 'A variant of the full NCBI36 human genome assembly used by the British Columbia Cancer Agency Genome Sciences Centre (BCCAGSC). <a href="../help/assemblies#NCBI36_BCCAGSC_variant">Click here for more detailed information</a>.',
    'Assembly:NCBI36_BCM_variant': 'A variant of the full NCBI36 human genome assembly used by Baylor College of Medicine Human Genome Sequencing Center. <a href="../help/assemblies#NCBI36_BCM_variant">Click here for more detailed information</a>.',
    'Assembly:NCBI36_WUGSC_variant': 'A variant of the full NCBI36 human genome assembly used by Washington University Genome Sequencing Center (WUGSC). <a href="../help/assemblies#NCBI36_WUGSC_variant">Click here for more detailed information</a>.',
    'Assembly:HG18': 'UCSC variant of NCBI human reference assembly build 36. <a href="../help/assemblies#HG18">Click here for more detailed information</a>.',
    'Assembly:HG18_Broad_variant': 'A variant of the NCBI36 human genome assembly used by the Broad Institute. <a href="../help/assemblies#HG18_Broad_variant">Click here for more detailed information</a>.',

    'Assembly:GRCh37': 'GRCh37 human genome assembly. <a href="../help/assemblies#GRCh37">Click here for more detailed information</a>.',
    'Assembly:GRCh37-lite-+-HPV_Redux-build': 'A variant of the GRCh37-lite human genome assembly used by the Broad Institute that includes the HPV viral genome. <a href="../help/assemblies#GRCh37-lite-+-HPV_Redux-build">Click here for more detailed information</a>.',
    'Assembly:GRCh37-lite': 'A subset of the full GRCh37 human genome assembly plus the human mitochondrial genome reference sequence. <a href="../help/assemblies#GRCh37-lite">Click here for more detailed information</a>.',
    'Assembly:GRCh37_BI_Variant': 'A variant of the GRCh37-lite human genome assembly used by the Broad Institute. <a href="../help/assemblies#GRCh37_BI_Variant">Click here for more detailed information</a>.',
    'Assembly:HG19': 'UCSC variant of GRCh37 human genome assembly. <a href="../help/assemblies#HG19">Click here for more detailed information</a>.',
    'Assembly:HG19_Broad_variant': 'A variant of the GRCh37 human genome assembly used by the Broad Institute. <a href="../help/assemblies#HG19_Broad_variant">Click here for more detailed information</a>.',

    ##
    # State
    ##
    'State:Bad data': 'Data file(s) failed the checksum process after being uploaded to CGHub',
    'State:Live': 'Data is available for downloaded',
    'State:Submitted': 'Metadata has passed validation but waiting on uploading of data file(s)',
    'State:Uploading': 'Uploading the data file(s) has started',
    'State:Validating sample': 'State during which additional sample metadata is collected from the DCC, before live',

    ##
    # Sample type
    ##
    'Sample Type:TP': 'Primary Solid Tumor (01)',
    'Sample Type:TR': 'Recurrent Solid Tumor (02)',
    'Sample Type:TB': 'Primary Blood Derived Cancer - Peripheral Blood (03)',
    'Sample Type:TRBM': 'Recurrent Blood Derived Cancer - Bone Marrow (04)',
    'Sample Type:TAP': 'Additional - New Primary (05)',
    'Sample Type:TM': 'Metastatic (06)',
    'Sample Type:TAM': 'Additional Metastatic (07)',
    'Sample Type:THOC': 'Human Tumor Original Cells (08)',
    'Sample Type:TBM': 'Primary Blood Derived Cancer - Bone Marrow (09)',
    'Sample Type:NB': 'Blood Derived Normal (10)',
    'Sample Type:NT': 'Solid Tissue Normal (11)',
    'Sample Type:NBC': 'Buccal Cell Normal (12)',
    'Sample Type:NEBV': 'EBV Immortalized Normal (13)',
    'Sample Type:NBM': 'Bone Marrow Normal (14)',
    'Sample Type:CELLC': 'Control Analyte (20)',
    'Sample Type:TRB': 'Recurrent Blood Derived Cancer - Peripheral Blood (40)',
    'Sample Type:CELL': 'Cell Lines (50)',
    'Sample Type:XP': 'Primary Xenograft Tissue (60)',
    'Sample Type:XCL': 'Cell Line Derived Xenograft Tissue (61)',

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
    'common:search-box': 'Text search of metadata. <a href="../help/assemblies#NCBI-human-build36">Click here for more detailed Information</a>.',
    'common:cghub-home-page-link': 'CGHub home page',
    
    ##
    # Cart
    ##
    'Remove from cart': 'Removes the selected items from the cart, one at a time or multiple items at once',
    'Clear cart': 'Removes all items from the cart',
    'Download manifest': 'Creates a manifest file (manifest.xml) that can be passed to GeneTorrent to download all the selected items in your cart',
    'Download metadata': 'Creates a file (metadata.xml) which contains a full dump of the metadata from selected items which you can parse offline',
    'Download summary TSV': 'Creates a summary of the basic metadata associated with each item in a tab-separated-value formatted file (TSV)',

    ##
    # metadata viewer
    ##
    'Show Metadata XML:': 'View the full metadata in XML format',
    'Collapse all': 'collapse all metadata XML on the screen',
    'Expand all': 'Expand all the metadata associated with the current item displayed',
    'Download XML': 'Download a complete XML file that can be displayed in your browser or pr',
}
