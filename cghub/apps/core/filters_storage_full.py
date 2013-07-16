"""
Storage file for filters

{
    'section_name': {
        'title': 'section_title',
        'filters': {
            'filter_value': 'filter_title',
        },
        'selectFilter': True,
    }
}

'filters' above are OrderedDict

For dates it has special format:

{
    'section_name': {
        'title': 'section_title',
        'filters': {
            'filter_value': {
                'filter_name': 'filter_title',
                'filter_id': 'filter_id'
            },
        'selectFilter': True,
        }
    }
}

'selectFilter' is True or unspecified, apply the select filter algorithm to
this filter.  Defaults to True in not specified.

"""

try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict


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
# TARGET studies are: phs000463 phs000464 phs000465 phs000466 phs000467 phs000468 phs000469 phs000471
#
# Keep names in sync with app/cghub/settings/help.py
#


# FIXME: would be good to have these as class

ALL_FILTERS = OrderedDict([
    ("study", {
        "title": "By Study",
        "filters": OrderedDict([
            ("phs000178", "TCGA"),
            ("*Other_Sequencing_Multiisolate", "CCLE"),
            ("phs0004*", "TARGET"),
            ('TCGA_MUT_BENCHMARK_4', 'TCGA Benchmark'),
        ]),
        "selectFilter": False,
    }),
    ("disease_abbr", {
        "title": "By Disease",
        "filters": OrderedDict([
            ("ACC",  "Adrenocortical carcinoma"),
            ("BLCA", "Bladder Urothelial Carcinoma"),
            ("BRCA", "Breast invasive carcinoma"),
            ("CESC", "Cervical squamous cell carcinoma and endocervical adenocarcinoma"),
            ("CNTL", "Controls"),
            ("COAD", "Colon adenocarcinoma"),
            ("DLBC", "Lymphoid Neoplasm Diffuse Large B-cell Lymphoma"),
            ("ESCA", "Esophageal carcinoma"),
            ("GBM",  "Glioblastoma multiforme"),
            ("HNSC", "Head and Neck squamous cell carcinoma"),
            ("KICH", "Kidney Chromophobe"),
            ("KIRC", "Kidney renal clear cell carcinoma"),
            ("KIRP", "Kidney renal papillary cell carcinoma"),
            ("LAML", "Acute Myeloid Leukemia"),
            ("LCLL", "Chronic Lymphocytic Leukemia"),
            ("LCML", "Chronic Myelogenous Leukemia"),
            ("LGG",  "Brain Lower Grade Glioma"),
            ("LIHC", "Liver hepatocellular carcinoma"),
            ("LUAD", "Lung adenocarcinoma"),
            ("LUSC", "Lung squamous cell carcinoma"),
            ("MESO", "Mesothelioma"),
            ("MISC", "Miscellaneous"),
            ("MM",   "Multiple Myeloma Plasma cell leukemia"),
            ("OV",   "Ovarian serous cystadenocarcinoma"),
            ("PAAD", "Pancreatic adenocarcinoma"),
            ("PCPG", "Pheochromocytoma and Paraganglioma"),
            ("PRAD", "Prostate adenocarcinoma"),
            ("READ", "Rectum adenocarcinoma"),
            ("SARC", "Sarcoma"),
            ("SKCM", "Skin Cutaneous Melanoma"),
            ("STAD", "Stomach adenocarcinoma"),
            ("THCA", "Thyroid carcinoma"),
            ("UCEC", "Uterine Corpus Endometrioid Carcinoma"),
            ("UCS",  "Uterine Carcinosarcoma"),
            ("UVM",  "Uveal Melanoma"),
        ]),
    }),
    ("sample_type", {
        "title": "By Sample Type",
        "filters": OrderedDict([
            ("07", "Additional Metastatic"),
            ("05", "Additional - New Primary"),
            ("10", "Blood Derived Normal"),
            ("14", "Bone Marrow Normal"),
            ("12", "Buccal Cell Normal"),
            ("61", "Cell Line Derived Xenograft Tissue"),
            ("50", "Cell Lines"),
            ("20", "Control Analyte"),
            ("13", "EBV Immortalized Normal"),
            ("08", "Human Tumor Original Cells"),
            ("06", "Metastatic"),
            ("09", "Primary Blood Derived Cancer - Bone Marrow"),
            ("03", "Primary Blood Derived Cancer - Peripheral Blood"),
            ("01", "Primary Solid Tumor"),
            ("60", "Primary Xenograft Tissue"),
            ("02", "Recurrent Solid Tumor"),
            ("04", "Recurrent Blood Derived Cancer - Bone Marrow"),
            ("40", "Recurrent Blood Derived Cancer - Peripheral Blood"),
            ("11", "Solid Tissue Normal"),
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
        }
    }),
    ("analyte_code", {
        "title": "By Experiment Type",
        "filters": OrderedDict([
            ("D", "DNA"),
            ("G", "GenomePlex"),
            ("H", "miRNA"),
            ("R", "RNA"),
            ("T", "Total RNA"),
            ("W", "WGA"),
            ("X", "WGA X"),
        ]),
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
            ("CGHUB", "CGHub"),
        ]),
        "selectFilter": False,
    }),
    ("platform", {
        "title": "By Platform",
        "filters": OrderedDict([
            ("LS454", "454"),
            ("ILLUMINA", "Illumina"),
            ("HELICOS", "Helicos"),
            ("ABI_SOLID", "ABI Solid"),
            ("COMPLETE_GENOMICS", "Complete Genomics"),
            ("PACBIO_SMRT", "Pacific Biosciences"),
            ("ION_TORRENT", "Ion Torrent"),
            ("CAPILLARY", "Capillary electrophoresis"),
        ])
    }),
    ('refassem_short_name', {
        'title': 'By Assembly',
        'filters': OrderedDict([
            ('NCBI36* OR HG18*', 'NCBI36/HG18 based'),
            ('GRCh37* OR HG19*', 'GRCh37/HG19 based'),
            ('NCBI-human-build36', 'NCBI-human-build36'),
            ('HG18', 'HG18'),
            ('HG18_Broad_variant', 'HG18_Broad_variant'),
            ('NCBI36_BCCAGSC_variant', 'NCBI36_BCCAGSC_variant'),
            ('NCBI36_BCM_variant', 'NCBI36_BCM_variant'),
            ('NCBI36_WUGSC_variant', 'NCBI36_WUGSC_variant'),
            ('GRCh37-lite-+-HPV_Redux-build', 'GRCh37-lite-+-HPV_Redux-build'),
            ('GRCh37-lite', 'GRCh37-lite'),
            ('GRCh37', 'GRCh37'),
            ('HG19', 'HG19'),
            ('GRCh37_BI_Variant', 'GRCh37_BI_Variant'),
            ('HG19_Broad_variant', 'HG19_Broad_variant'),
        ]),
        "selectFilter": False,
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
        "selectFilter": False,
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
        "selectFilter": False,
    }),
    ("state", {
        "title": "By State",
        "filters": OrderedDict([
            ("live", "Live"),
            ("suppressed", "Suppressed"),
            ("redacted", "Redacted"),
            ("submitted", "Submitted"),
            ("uploading", "Uploading"),
            ("validating_data", "Validating data"),
            ("validating_sample", "Validating sample"),
            ("augmenting_data", "Augmenting data"),
            ("bad_data", "Bad data"),
        ]),
        "selectFilter": False,
    }),
])
