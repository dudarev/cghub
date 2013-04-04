# -*- coding: utf-8 -*-
"""
cghub.settings.wsapi
~~~~~~~~~~~~~~~~~~~~

This module provides settings for wsapi app.

Settings:

    :param WSAPI_CGHUB_SERVER: CGHub server url
    :param WSAPI_CGHUB_ANALYSIS_ID_URI: Analysis Object Identification uri
    :param CGHUB_ANALYSIS_DETAIL_URI: Complete set of attributes uri
    :param CGHUB_ANALYSIS_FULL_URI: Complete set of attributes and submission metadata uri
    :param WSAPI_CACHE_DIR: directory to store cache, ``/tmp/wsapi/`` by default
    :param WSAPI_USE_CACHE: enables caching if equals True, False is the default
    :param WSAPI_CACHE_BACKEND: determines cache type, for now available types are ('simple',)

"""

WSAPI_CGHUB_SERVER = 'https://cghub.ucsc.edu'
WSAPI_CGHUB_ANALYSIS_ID_URI = '/cghub/metadata/analysisId'
WSAPI_CGHUB_ANALYSIS_DETAIL_URI = '/cghub/metadata/analysisDetail'
WSAPI_CGHUB_ANALYSIS_FULL_URI = '/cghub/metadata/analysisFull'
WSAPI_USE_CACHE = True
WSAPI_CACHE_BACKEND = 'simple'
WSAPI_CACHE_DIR = '/tmp/wsapi/'
