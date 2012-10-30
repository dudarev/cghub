# -*- coding: utf-8 -*-
import datetime
"""
wsapi.settings
~~~~~~~~~~~~~~~~~~~~

This module provides the some default settings.

Settings:

    :CACHE_DIR: directory to store cache, ``/tmp/wsapi/`` by default
    :USE_CACHE: enables caching if equals True, False is the default
    :CACHE_BACKEND: determines cache type, for now available types are ('simple',)

"""

USE_CACHE = True

CACHE_BACKEND = 'simple'
CACHE_DIR = '/tmp/wsapi/'

TIME_DELETE_API_CACHE_FILES_OLDER = datetime.timedelta(minutes=2)
TIME_CHECK_API_CACHE_INTERVAL = datetime.timedelta(minutes=1) 
