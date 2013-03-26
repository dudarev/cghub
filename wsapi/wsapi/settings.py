# -*- coding: utf-8 -*-
"""
wsapi.settings
~~~~~~~~~~~~~~~~~~~~

This module provides default settings.

Settings:

    :CGHUB_SERVER: CGHub server url
    :CGHUB_ANALYSIS_ID_URI: Analysis Object Identification uri
    :CGHUB_ANALYSIS_FULL_URI: Complete set of attributes uri
    :CACHE_DIR: directory to store cache, ``/tmp/wsapi/`` by default
    :USE_CACHE: enables caching if equals True, False is the default
    :CACHE_BACKEND: determines cache type, for now available types are ('simple',)

"""

SETTINGS_DEFAULT = dict(
    CGHUB_SERVER='https://cghub.ucsc.edu',
    CGHUB_ANALYSIS_ID_URI='/cghub/metadata/analysisId',
    CGHUB_ANALYSIS_FULL_URI='/cghub/metadata/analysisFull',
    USE_CACHE=True,
    CACHE_BACKEND='simple',
    CACHE_DIR='/tmp/wsapi/',
)
