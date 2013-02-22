# -*- coding: utf-8 -*-
"""
cghub.settings.wsapi
~~~~~~~~~~~~~~~~~~~~

This module provides settings for wsapi app.

Settings:

    :WSAPI_CGHUB_SERVER: CGHub server url
    :WSAPI_CGHUB_ANALYSIS_ID_URI: Analysis Object Identification uri
    :WSAPI_CGHUB_ANALYSIS_ATTRIBUTES_URI: Analysis Attribute Query uri
    :WSAPI_CACHE_DIR: directory to store cache, ``/tmp/wsapi/`` by default
    :WSAPI_USE_CACHE: enables caching if equals True, False is the default
    :WSAPI_CACHE_BACKEND: determines cache type, for now available types are ('simple',)

"""

WSAPI_CGHUB_SERVER='https://cghub.ucsc.edu'
WSAPI_CGHUB_ANALYSIS_ID_URI='/cghub/metadata/analysisId'
WSAPI_CGHUB_ANALYSIS_ATTRIBUTES_URI='/cghub/metadata/analysisAttributes'
WSAPI_USE_CACHE=True
WSAPI_CACHE_BACKEND='simple'
WSAPI_CACHE_DIR='/tmp/wsapi/'


WSAPI_SETTINGS = {
    'CGHUB_SERVER': WSAPI_CGHUB_SERVER,
    'CGHUB_ANALYSIS_ID_URI': WSAPI_CGHUB_ANALYSIS_ID_URI,
    'CGHUB_ANALYSIS_ATTRIBUTES_URI': WSAPI_CGHUB_ANALYSIS_ATTRIBUTES_URI,
    'USE_CACHE': WSAPI_USE_CACHE,
    'CACHE_BACKEND': WSAPI_CACHE_BACKEND,
    'CACHE_DIR': WSAPI_CACHE_DIR,
}
