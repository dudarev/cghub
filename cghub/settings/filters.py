"""
Storage file for filters

{
    'section_name': {
        'title': 'section_title',
        'filters': {
            'filter_title': 'filter_value',
        },
        'selectOptions': True,
    }
}

'filters' above are OrderedDict

Hierarchical filters are supported, example:

('refassem_short_name', {
    'title': 'By Assembly',
    'filters': OrderedDict([
        ('NCBI36/HG18', OrderedDict([
            ('NCBI-human-build36', 'NCBI-human-build36'),
            ('NCBI36_BCCAGSC_variant', 'NCBI36_BCCAGSC_variant'),
            ('NCBI36_BCM_variant', 'NCBI36_BCM_variant'),
        ])),
        ('GRCh37/HG19', OrderedDict([
            ('GRCh37', 'GRCh37'),
            ('GRCh37-lite', 'GRCh37-lite'),
            ('GRCh37_BI_Variant', 'GRCh37_BI_Variant'),
        ])),
        ('unaligned', 'unaligned'),
    ]),
    "selectOptions": True,
})

For dates it has special format:

{
    'section_name': {
        'title': 'section_title',
        'filters': {
            'filter_value': {
                'filter_title': 'filter_name',
                'filter_id': 'filter_id'
            },
        'selectOptions': True,
        }
    }
}

If 'selectOptions' is True or unspecified, apply the select options algorithm to this filter
(used by ``selectoptions`` management command).
If 'searchForNewOptions' is True, will be scanned all options and displayed missing ones.
(used by ``searchoptions`` management command)

If filter name starts from 'INVISIBLE', it will be not displayed even if it will be found.

OR statement are allowed.
(for example: "phs0004* OR phs000218") (wildcart at end and start of string is supported).
"""

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.simplejson import OrderedDict


DATE_FILTERS_HTML_IDS = OrderedDict([
    ("", "id_date_any"),
    ("[NOW-1DAY TO NOW]", "id_date_today"),
    ("[NOW-7DAY TO NOW]", "id_date_week"),
    ("[NOW-1MONTH TO NOW]", "id_date_month"),
    ("[NOW-1YEAR TO NOW]", "id_date_year"),
])

# TCGA descriptions should match those in codeTablesReport when possible:
#   https://tcga-data.nci.nih.gov/datareports/codeTablesReport.htm
#
# TARGET parent study is: phs000218
# TARGET sub-studies are: phs000463 phs000464 phs000465 phs000466 phs000467 phs000468 phs000469 phs000471
#
# Keep names in sync with app/cghub/settings/help.py
#


# FIXME: would be good to have these as class

ALL_FILTERS = OrderedDict([
    ("study", {
        "title": "By Study",
        "filters": OrderedDict([
            ("TCGA", "phs000178"),
            ("CCLE", "*Other_Sequencing_Multiisolate"),
            ("TARGET", "phs0004* OR phs000218"),
            ("TCGA Benchmark", "TCGA_MUT_BENCHMARK_4"),
            ("INVISIBLE_CGTEST", "CGTEST"),
            ("INVISIBLE_TEST_CGI_CHECK", "TEST_CGI_CHECK"),
            ("INVISIBLE_CGHUB_PERFORMANCE_TESTING", "CGHUB_PERFORMANCE_TESTING"),
        ]),
        "selectOptions": True,
        "searchForNewOptions": True,
    }),
    ("disease_abbr", {
        "title": "By Disease",
        "filters": OrderedDict([
            ("Acute Lymphoblastic Leukemia", "ALL"),
            ("Acute Myeloid Leukemia", "LAML OR AML"),
            ("Adrenocortical carcinoma", "ACC"),
            ("Bladder Urothelial Carcinoma", "BLCA"),
            ("Brain Lower Grade Glioma", "LGG"),
            ("Breast invasive carcinoma", "BRCA"),
            ("Cervical squamous cell carcinoma and endocervical adenocarcinoma", "CESC"),
            ("Chronic Lymphocytic Leukemia", "LCLL"),
            ("Chronic Myelogenous Leukemia", "LCML"),
            ("Clear Cell Sarcoma of the Kidney", "CCSK"),
            ("Colon adenocarcinoma", "COAD"),
            ("Controls", "CNTL"),
            ("Esophageal carcinoma", "ESCA"),
            ("Glioblastoma multiforme", "GBM"),
            ("Head and Neck squamous cell carcinoma", "HNSC"),
            ("Kidney Chromophobe", "KICH"),
            ("Kidney renal clear cell carcinoma", "KIRC"),
            ("Kidney renal papillary cell carcinoma", "KIRP"),
            ("Liver hepatocellular carcinoma", "LIHC"),
            ("Lung adenocarcinoma", "LUAD"),
            ("Lung squamous cell carcinoma", "LUSC"),
            ("Lymphoid Neoplasm Diffuse Large B-cell Lymphoma", "DLBC"),
            ("Mesothelioma", "MESO"),
            ("Miscellaneous", "MISC"),
            ("Multiple Myeloma Plasma cell leukemia", "MM"),
            ("Neuroblastoma", "NBL"),
            ("Osteosarcoma", "OS"),
            ("Ovarian serous cystadenocarcinoma", "OV"),
            ("Pancreatic adenocarcinoma", "PAAD"),
            ("Pheochromocytoma and Paraganglioma", "PCPG"),
            ("Prostate adenocarcinoma", "PRAD"),
            ("Rectum adenocarcinoma", "READ"),
            ("Sarcoma", "SARC"),
            ("Skin Cutaneous Melanoma", "SKCM"),
            ("Stomach adenocarcinoma", "STAD"),
            ("Thyroid carcinoma", "THCA"),
            ("Uterine Carcinosarcoma", "UCS"),
            ("Uterine Corpus Endometrioid Carcinoma", "UCEC"),
            ("Uveal Melanoma", "UVM"),
            ("Wilms Tumor", "WT"),
            ("INVISIBLE_TEST", "TEST"),
        ]),
        "selectOptions": True,
        "searchForNewOptions": True,
    }),
    ("sample_type", {
        "title": "By Sample Type",
        "filters": OrderedDict([
            ("Additional Metastatic", "07 OR TARGET_07"),
            ("Additional - New Primary", "05 OR TARGET_05"),
            ("Blood Derived Normal", "10 OR TARGET_10"),
            ("Bone Marrow Normal", "14 OR TARGET_14"),
            ("Buccal Cell Normal", "12 OR TARGET_12"),
            ("Cell Line Derived Xenograft Tissue", "61 OR TARGET_61"),
            ("Cell Lines", "50 OR TARGET_50"),
            ("Control Analyte", "20 OR TARGET_20"),
            ("EBV Immortalized Normal", "13 OR TARGET_13"),
            ("Fibroblast Normal", "TARGET_15"),
            ("Granulocytes", "TARGET_99"),
            ("Human Tumor Original Cells", "08"),
            ("Metastatic", "06 OR TARGET_06"),
            ("Post neo-adjuvant therapy", "TARGET_08"),
            ("Post treatment Blood Cancer - Blood", "TARGET_42"),
            ("Post treatment Blood Cancer - Bone Marrow", "TARGET_41"),
            ("Primary Blood Derived Cancer - Bone Marrow", "09 OR TARGET_09"),
            ("Primary Blood Derived Cancer - Peripheral Blood", "03 OR TARGET_03"),
            ("Primary Solid Tumor", "01 OR TARGET_01"),
            ("Primary Xenograft Tissue", "60 OR TARGET_60"),
            ("Recurrent Solid Tumor", "02 OR TARGET_02"),
            ("Recurrent Blood Derived Cancer - Bone Marrow", "04 OR TARGET_04"),
            ("Recurrent Blood Derived Cancer - Peripheral Blood", "40 OR TARGET_40"),
            ("Solid Tissue Normal", "11 OR TARGET_11"),
        ]),
        "shortcuts": {
            "01": "TP",
            "02": "TR",
            "03": "TB",
            "04": "TRBM",
            "05": "TAP",
            "06": "TM",
            "07": "TAM",
            "08": "THOC",
            "09": "TBM",
            "10": "NB",
            "11": "NT",
            "12": "NBC",
            "13": "NEBV",
            "14": "NBM",
            "20": "CELLC",
            "40": "TRB",
            "50": "CELL",
            "60": "XP",
            "61": "XCL",
            # TARGET does not have standard abbreviations, when one is not defined from TCGA,
            # we generated one as lower-case
            "TARGET_01": "TP",
            "TARGET_02": "TR",
            "TARGET_03": "TB",
            "TARGET_04": "TRBM",
            "TARGET_05": "TAP",
            "TARGET_06": "TM",
            "TARGET_07": "TAM",
            "TARGET_08": "pnat",
            "TARGET_09": "TBM",
            "TARGET_10": "NB",
            "TARGET_11": "NT",
            "TARGET_12": "NBC",
            "TARGET_13": "NEBV",
            "TARGET_14": "NBM",
            "TARGET_15": "fn",
            "TARGET_20": "CELLC",
            "TARGET_40": "TRB",
            "TARGET_41": "tbpt",
            "TARGET_42": "bmpt",
            "TARGET_50": "CELL",
            "TARGET_60": "XP",
            "TARGET_61": "XCL",
            "TARGET_99": "gran",
        },
        "selectOptions": True,
        "searchForNewOptions": True,
        
    }),
    ("analyte_code", {
        "title": "By Analyte Type",
        "filters": OrderedDict([
            ("DNA", "D"),
            ("GenomePlex", "G"),
            ("miRNA", "H"),
            ("RNA", "R"),
            ("Total RNA", "T"),
            ("WGA", "W"),
            ("WGA X", "X"),
        ]),
        "selectOptions": True,
        "searchForNewOptions": True,
    }),
    ("library_strategy", {
        "title": "By Library Type",
        "filters": OrderedDict([
            ("AMPLICON", "AMPLICON"),
            ("Bisulfite-Seq", "Bisulfite-Seq"),
            ("CLONE", "CLONE"),
            ("CLONEEND", "CLONEEND"),
            ("CTS", "CTS"),
            ("ChIA-PET", "ChIA-PET"),
            ("ChIP-Seq", "ChIP-Seq"),
            ("DNase-Hypersensitivity", "DNase-Hypersensitivity"),
            ("EST", "EST"),
            ("FAIRE-seq", "FAIRE-seq"),
            ("FINISHING", "FINISHING"),
            ("FL-cDNA", "FL-cDNA"),
            ("MBD-Seq", "MBD-Seq"),
            ("MNase-Seq", "MNase-Seq"),
            ("MRE-Seq", "MRE-Seq"),
            ("MeDIP-Seq", "MeDIP-Seq"),
            ("OTHER", "OTHER"),
            ("POOLCLONE", "POOLCLONE"),
            ("RIP-Seq", "RIP-Seq"),
            ("RNA-Seq", "RNA-Seq"),
            ("SELEX", "SELEX"),
            ("Tn-Seq", "Tn-Seq"),
            ("VALIDATION", "VALIDATION"),
            ("WCS", "WCS"),
            ("WGA", "WGA"),
            ("WGS", "WGS"),
            ("WXS", "WXS"),
            ("miRNA-Seq", "miRNA-Seq"),
            ("ncRNA-Seq", "ncRNA-Seq"),
        ]),
        "selectOptions": True,
        "searchForNewOptions": True,
    }),
    ("center_name", {
        "title": "By Center",
        "filters": OrderedDict([
            ("BCM", "BCM"),
            ("BCCAGSC", "BCCAGSC"),
            ("BI", "BI"),
            ("HMS-RK", "HMS-RK"),
            ("UCSC", "UCSC"),
            ("UNC-LCCC", "UNC-LCCC"),
            ("USC-JHU", "USC-JHU"),
            ("WUGSC", "WUGSC"),
            ("Complete Genomics", "CompleteGenomics"),
            ("INVISIBLE_CGHUB", "CGHUB")
        ]),
        "selectOptions": True,
        "searchForNewOptions": True,
    }),
    ("platform", {
        "title": "By Platform",
        "filters": OrderedDict([
            ("454", "LS454"),
            ("Illumina", "ILLUMINA"),
            ("Helicos", "HELICOS"),
            ("ABI Solid", "ABI_SOLID"),
            ("Complete Genomics", "COMPLETE_GENOMICS"),
            ("Pacific Biosciences", "PACBIO_SMRT"),
            ("Ion Torrent", "ION_TORRENT"),
            ("Capillary electrophoresis", "CAPILLARY"),
        ]),
        "selectOptions": True,
        "searchForNewOptions":True,
    }),
    ('refassem_short_name', {
        'title': 'By Assembly',
        'filters': OrderedDict([
            ('NCBI36/HG18', OrderedDict([
                ('NCBI-human-build36', 'NCBI-human-build36'),
                ('NCBI36_BCCAGSC_variant', 'NCBI36_BCCAGSC_variant'),
                ('NCBI36_BCM_variant', 'NCBI36_BCM_variant'),
                ('NCBI36_WUGSC_variant', 'NCBI36_WUGSC_variant'),
                ('HG18', 'HG18'),
                ('HG18_Broad_variant', 'HG18_Broad_variant'),
            ])),
            ('GRCh37/HG19', OrderedDict([
                ('GRCh37', 'GRCh37'),
                ('GRCh37-lite', 'GRCh37-lite'),
                ('GRCh37_BI_Variant', 'GRCh37_BI_Variant'),
                ('GRCh37-lite-+-HPV_Redux-build', 'GRCh37-lite-+-HPV_Redux-build'),
                ('HG19', 'HG19'),
                ('HG19_Broad_variant', 'HG19_Broad_variant'),
            ])),
            ('unaligned', 'unaligned'),
        ]),
        "selectOptions": True,
        "searchForNewOptions": True,
    }),
    ('preservation_method', {
        "title": "By Preservation Method",
        "filters": OrderedDict([
            ("FFPE", "ffpe"),
            ("frozen", "frozen"),
        ]),
        "selectOptions": False,
    }),
    ('upload_date', {
        'title': 'By Upload Date',
        'filters': OrderedDict([
            ('', {
                'filter_id': 'id_date_any',
                'filter_name': 'Any date',
            }),
            ('[NOW-1DAY TO NOW]', {
                'filter_id': 'id_date_today',
                'filter_name': 'Today',
            }),
            ('[NOW-7DAY TO NOW]', {
                'filter_id': 'id_date_week',
                'filter_name': 'Last week',
            }),
            ('[NOW-1MONTH TO NOW]', {
                'filter_id': 'id_date_month',
                'filter_name': 'Last month',
            }),
            ('[NOW-1YEAR TO NOW]', {
                'filter_id': 'id_date_year',
                'filter_name': 'Last 12 months',
            }),
        ]),
        "selectOptions": False,
    }),
    ("last_modified", {
        "title": "By Modification Date",
        "filters": OrderedDict([
            ("", {
                'filter_name': "Any date",
                'filter_id': "id_date_any"}),
            ("[NOW-1DAY TO NOW]", {
                "filter_name": "Today",
                "filter_id": "id_date_today"}),
            ("[NOW-7DAY TO NOW]", {
                "filter_name": "Last week",
                "filter_id": "id_date_week"}),
            ("[NOW-1MONTH TO NOW]", {
                "filter_name": "Last month",
                "filter_id": "id_date_month"}),
            ("[NOW-1YEAR TO NOW]", {
                "filter_name": "Last 12 months",
                "filter_id": "id_date_year"}),
        ]),
        "selectOptions": False,
    }),
    ("state", {
        "title": "By State",
        "filters": OrderedDict([
            ("Live", "live"),
            ("Suppressed", "suppressed"),
            ("Redacted", "redacted"),
            ("Submitted", "submitted"),
            ("Uploading", "uploading"),
            ("Validating data", "validating_data"),
            ("Validating sample", "validating_sample"),
            ("Augmenting data", "augmenting_data"),
            ("Bad data", "bad_data"),
        ]),
        "selectOptions": False,
        "searchForNewOptions": True,
    }),
])
