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

'filters' above are OrderedDict

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

ALL_FILTERS = OrderedDict([
    ('study', {
        'filters': OrderedDict([
            ('phs000178', 'TCGA'),
            ('TCGA_MUT_BENCHMARK_4', 'TCGA Benchmark'),
        ]),
        'title': 'By Study',
    }),
    ('center_name', {
        'filters': OrderedDict([
            ('BCM', 'Baylor'),
            ('BCCAGSC', 'BCCAGSC'),
            ('BI', 'Broad Institute'),
            ('HMS-RK', 'Harvard'),
            ('UNC-LCCC', 'UNC-LCCC'),
            ('USC-JHU', 'USC/Sidney K. B.'),
            ('WUGSC', 'Washington U.'),
        ]),
        'title': 'By Center',
    }),
    ('analyte_code', {
        'filters': OrderedDict([
            ('D', 'DNA'),
            ('H', 'mirVana RNA'),
            ('R', 'RNA'),
            ('T', 'Total RNA'),
            ('W', 'WGA'),
        ]),
        'title': 'By Experiment Type',
    }),
    ('upload_date', {
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
                'filter_name': 'This week',
            }),
            ('[NOW-1MONTH TO NOW]', {
                'filter_id': 'id_date_month',
                'filter_name': 'This month',
            }),
            ('[NOW-1YEAR TO NOW]', {
                'filter_id': 'id_date_year',
                'filter_name': 'This year',
            }),
        ]),
        'title': 'By Upload Time',
    }),
    ('last_modified', {
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
                'filter_name': 'This week',
            }),
            ('[NOW-1MONTH TO NOW]', {
                'filter_id': 'id_date_month',
                'filter_name': 'This month',
            }),
            ('[NOW-1YEAR TO NOW]', {
                'filter_id': 'id_date_year',
                'filter_name': 'This year',
            }),
        ]),
        'title': 'By Time Modified',
    }),
    ('sample_type', {
        'shortcuts': {
            '02': 'TR',
            '03': 'TB',
            '13': 'NEBV',
            '01': 'TP',
            '06': 'TM',
            '07': 'TAM',
            '04': 'TRBM',
            '05': 'TAP',
            '08': 'THOC',
            '09': 'TBM',
            '50': 'CELL',
            '40': 'TRB',
            '60': 'XP',
            '61': 'XCL',
            '12': 'NBC',
            '14': 'NBM',
            '11': 'NT',
            '20': 'CELLC',
            '10': 'NB',
        },
        'filters': OrderedDict([
            ('10', 'Blood Derived Normal'),
            ('12', 'Buccal Cell Normal'),
            ('20', 'Control Analyte'),
            ('06', 'Metastatic'),
            ('03', 'Primary Blood Derived Cancer - Peripheral Blood'),
            ('01', 'Primary solid Tumor'),
            ('02', 'Recurrent Solid Tumor'),
            ('11', 'Solid Tissue Normal'),
        ]),
        'title': 'By Sample Type',
    }),
    ('library_strategy', {
        'filters': OrderedDict([
            ('Bisulfite-Seq', 'Bisulfite-Seq'),
            ('OTHER', 'OTHER'),
            ('RNA-Seq', 'RNA-Seq'),
            ('WGS', 'WGS'),
            ('WXS', 'WXS'),
        ]),
        'title': 'By Run Type',
    }),
    ('refassem_short_name', {
        'filters': OrderedDict([
            ('NBCI36*', 'NBCI36'),
            ('HG18*', 'HG18'),
            ('GRCh37*', 'GRCh37'),
            ('HG19*', 'HG19'),
        ]),
        'title': 'By Assembly',
    }),
    ('disease_abbr', {
        'filters': OrderedDict([
            ('LAML', 'Acute Myeloid Leukemia'),
            ('BLCA', 'Bladder Urothelial Carcinoma'),
            ('LGG', 'Brain Lower Grade Glioma'),
            ('BRCA', 'Breast invasive carcinoma'),
            ('CESC', 'Cervical squamous cell carcinoma and endocervical adenocarcinoma'),
            ('COAD', 'Colon adenocarcinoma'),
            ('CNTL', 'Controls'),
            ('GBM', 'Glioblastoma multiforme'),
            ('HNSC', 'Head and Neck squamous cell carcinoma'),
            ('KIRC', 'Kidney renal clear cell carcinoma'),
            ('KIRP', 'Kidney renal papillary cell carcinoma'),
            ('LIHC', 'Liver hepatocellular carcinoma'),
            ('LUAD', 'Lung adenocarcinoma'),
            ('LUSC', 'Lung squamous cell carcinoma'),
            ('OV', 'Ovarian serous cystadenocarcinoma'),
            ('PAAD', 'Pancreatic adenocarcinoma'),
            ('PRAD', 'Prostate adenocarcinoma'),
            ('READ', 'Rectum adenocarcinoma'),
            ('SKCM', 'Skin Cutaneous Melanoma'),
            ('STAD', 'Stomach adenocarcinoma'),
            ('THCA', 'Thyroid carcinoma'),
            ('UCEC', 'Uterine Corpus Endometrioid Carcinoma'),
        ]),
        'title': 'By Disease',
    }),
    ("state", {
        "filters": OrderedDict([
            ("bad_data", "Bad data"),
            ("live", "Live"),
            ("submitted", "Submitted"),
            ("supressed", "Supressed"),
            ("uploading", "Uploading"),
            ("validating_data", "Validating data"),
            ("validating_sample", "Validating sample"),
        ]),
        "title": "By State",
    })
])
# end of ALL_FILTERS
# do not remove this comment, it is used in selectfilters
