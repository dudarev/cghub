# -*- coding: utf-8 -*-
"""
wsapi.settings
~~~~~~~~~~~~~~~~~~~~

This module provides the some default settings.

Settings:

    :CGHUB_SERVER: CGHub server url
    :CGHUB_ANALYSIS_ID_URI: Analysis Object Identification uri
    :CGHUB_ANALYSIS_ATTRIBUTES_URI: Analysis Attribute Query uri
    :CACHE_DIR: directory to store cache, ``/tmp/wsapi/`` by default
    :USE_CACHE: enables caching if equals True, False is the default
    :USE_API_LIGHT: use api_light for large querires
    :CACHE_BACKEND: determines cache type, for now available types are ('simple',)

"""

CGHUB_SERVER = 'https://cghub.ucsc.edu'
CGHUB_ANALYSIS_ID_URI = '/cghub/metadata/analysisId'
CGHUB_ANALYSIS_ATTRIBUTES_URI = '/cghub/metadata/analysisAttributes'

USE_CACHE = True
USE_API_LIGHT = False

CACHE_BACKEND = 'simple'
CACHE_DIR = '/tmp/wsapi/'

try:
    from settings_local import *
except ImportError:
    pass
