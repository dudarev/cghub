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
"""

DATE_FILTERS_HTML_IDS = {
    "": "id_date_any",
    "[NOW-1DAY TO NOW]": "id_date_today",
    "[NOW-7DAY TO NOW]": "id_date_week",
    "[NOW-1MONTH TO NOW]": "id_date_month",
    "[NOW-1YEAR TO NOW]": "id_date_year",
}

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
            "H": "mirVana RNAmirVana RNARNA",
            "R": "RNA",
            "T": "Total RNA",
            "W": "WGA",
            "X": "WGA X",
        },
    },
    "last_modified": {
        "title": "By Date Uploaded",
        "filters": {
            "": "Any date",
            "[NOW-1DAY TO NOW]": "Today",
            "[NOW-7DAY TO NOW]": "This week",
            "[NOW-1MONTH TO NOW]": "This month",
            "[NOW-1YEAR TO NOW]": "This year",
        },
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
