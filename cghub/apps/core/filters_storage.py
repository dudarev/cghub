try:
    from collections import OrderedDict
except ImportError:
    from celery.utils.compat import OrderedDict
"""
Storage file for filters

{
    'section_name': {
        'title': 'section_title',
        'filters': {
            'filter_value': 'filter_title',
        }
    }
}

For dates it has special format:

{
    'section_name': {
        'title': 'section_title',
        'filters': {
            'filter_value': {
                'filter_name': 'filter_title',
                'filter_id': 'filter_id'
            }
        }
    }
}

"""

DATE_FILTERS_HTML_IDS = OrderedDict([
    ("", "id_date_any"),
    ("[NOW-1DAY TO NOW]", "id_date_today"),
    ("[NOW-7DAY TO NOW]", "id_date_week"),
    ("[NOW-1MONTH TO NOW]", "id_date_month"),
    ("[NOW-1YEAR TO NOW]", "id_date_year"),
])

ALL_FILTERS = {
    "center_name": {
        "title": "By Center",
        "filters": {
            "BCM": "Baylor",
            "BCCAGSC": "BCCAGSC",
            "BI": "Broad Institute",
            "HMS-RK": "Harvard",
            "UNC-LCCC": "UNC-LCCC",
            "USC-JHU": "USC/Sidney K. B.",
            "WUGSC": "Washington U.",
        },
    },
    "analyte_code": {
        "title": "By Experiment Type",
        "filters": {
            "D": "DNA",
            "G": "GenomePlex",
            "H": "mirVana RNA",
            "R": "RNA",
            "T": "Total RNA",
            "W": "WGA",
            "X": "WGA X",
        },
    },
    "last_modified": {
        "title": "By Date Uploaded",
        "filters": OrderedDict([
            ("", {
                'filter_name': "Any date",
                'filter_id': "id_date_any"}),
            ("[NOW-1DAY TO NOW]", {
                "filter_name": "Today",
                "filter_id": "id_date_today"}),
            ("[NOW-7DAY TO NOW]", {
                "filter_name": "This week",
                "filter_id": "id_date_week"}),
            ("[NOW-1MONTH TO NOW]", {
                "filter_name": "This month",
                "filter_id": "id_date_month"}),
            ("[NOW-1YEAR TO NOW]", {
                "filter_name": "This year",
                "filter_id": "id_date_year"}),
        ]),
    },
    "sample_type": {
        "title": "By Sample Type",
        "filters": {
            "01": "Primary solid Tumor",
            "02": "Recurrent Solid Tumor",
            "03": "Primary Blood Derived Cancer - Peripheral Blood",
            "04": "Recurrent Blood Derived Cancer - Bone Marrow",
            "05": "Additional - New Primary",
            "06": "Metastatic",
            "07": "Additional Metastatic",
            "08": "Human Tumor Original Cells",
            "09": "Primary Blood Derived Cancer - Bone Marrow",
            "10": "Blood Derived Normal",
            "11": "Solid Tissue Normal",
            "12": "Buccal Cell Normal",
            "13": "EBV Immortalized Normal",
            "14": "Bone Marrow Normal",
            "20": "Control Analyte",
            "40": "Recurrent Blood Derived Cancer - Peripheral Blood",
            "50": "Cell Lines",
            "60": "Primary Xenograft Tissue",
            "61": "Cell Line Derived Xenograft Tissue",
        },
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
    },
    "library_strategy": {
        "title": "By Run Type",
        "filters": {
            "WGS": "WGS",
            "WXS": "WXS",
            "RNA-Seq": "RNA-Seq",
            "WCS": "WCS",
            "CLONE": "CLONE",
            "POOLCLONE": "POOLCLONE",
            "AMPLICON": "AMPLICON",
            "CLONEEND": "CLONEEND",
            "FINISHING": "FINISHING",
            "ChIP-Seq": "ChIP-Seq",
            "MNase-Seq": "MNase-Seq",
            "DNase-Hypersensitivity": "DNase-Hypersensitivity",
            "Bisulfite-Seq": "Bisulfite-Seq",
            "EST": "EST",
            "FL-cDNA": "FL-cDNA",
            "CTS": "CTS",
            "MRE-Seq": "MRE-Seq",
            "MeDIP-Seq": "MeDIP-Seq",
            "MDB-Seq": "MDB-Seq",
            "OTHER": "OTHER",
        },
    },
    "disease_abbr": {
        "title": "By Disease",
        "filters": {
            "LAML": "Acute Myeloid Leukemia",
            "BLCA": "Bladder Urothelial Carcinoma",
            "LGG": "Brain Lower Grade Glioma",
            "BRCA": "Breast invasive carcinoma",
            "CESC": "Cervical squamous cell carcinoma and endocervical adenocarcinoma",
            "LCLL": "Chronic Lymphocytic Leukemia",
            "COAD": "Colon adenocarcinoma",
            "CNTL": "Controls",
            "ESCA": "Esophageal carcinoma",
            "GBM": "Glioblastoma multiforme",
            "HNSC": "Head and Neck squamous cell carcinoma",
            "KICH": "Kidney Chromophobe",
            "KIRC": "Kidney renal clear cell carcinoma",
            "KIRP": "Kidney renal papillary cell carcinoma",
            "LIHC": "Liver hepatocellular carcinoma",
            "LUAD": "Lung adenocarcinoma",
            "LUSC": "Lung squamous cell carcinoma",
            "DLBC": "Lymphoid Neoplasm Diffuse Large B-cell Lymphoma",
            "OV": "Ovarian serous cystadenocarcinoma",
            "PAAD": "Pancreatic adenocarcinoma",
            "PRAD": "Prostate adenocarcinoma",
            "READ": "Rectum adenocarcinoma",
            "SARC": "Sarcoma",
            "SKCM": "Skin Cutaneous Melanoma",
            "STAD": "Stomach adenocarcinoma",
            "THCA": "Thyroid carcinoma",
            "UCEC": "Uterine Corpus Endometrioid Carcinoma",
        },
    },
}
