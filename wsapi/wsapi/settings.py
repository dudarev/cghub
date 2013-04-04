# -*- coding: utf-8 -*-
"""
wsapi.settings
~~~~~~~~~~~~~~~~~~~~

This module provides default settings.

Settings:

    :param CGHUB_SERVER: CGHub server url
    :param CGHUB_ANALYSIS_ID_URI: Analysis Object Identification uri
    :param CGHUB_ANALYSIS_DETAIL_URI: Complete set of attributes uri
    :param CGHUB_ANALYSIS_FULL_URI: Complete set of attributes and submission metadata uri
    :param CACHE_DIR: directory to store cache, ``/tmp/wsapi/`` by default
    :param USE_CACHE: enables caching if equals True, False is the default
    :param CACHE_BACKEND: determines cache type, for now available types are ('simple',)

"""

SETTINGS_DEFAULT = dict(
    CGHUB_SERVER='https://cghub.ucsc.edu',
    CGHUB_ANALYSIS_ID_URI='/cghub/metadata/analysisId',
    CGHUB_ANALYSIS_DETAIL_URI='/cghub/metadata/analysisDetail',
    CGHUB_ANALYSIS_FULL_URI='/cghub/metadata/analysisFull',
    USE_CACHE=True,
    CACHE_BACKEND='simple',
    CACHE_DIR='/tmp/wsapi/',
)
