# -*- coding: utf-8 -*-
"""
cghub.settings.api
~~~~~~~~~~~~~~~~~~~~

This module provides settings for cghub-python-api.

Settings:

    :param CGHUB_SERVER: CGHub server url
    :param CGHUB_SERVER_SOLR_URI: cghub server uri. Used only by SOLRRequest
    :param API_HTTP_ERROR_ATTEMPTS: number of attempts to connect to server after HTTP503 was raised
    :param API_HTTP_ERROR_SLEEP_AFTER: number of seconds to wait before next attempt to connect to server after HTTP503 was raised
    :param API_TYPE: SOLR or WSAPI
"""

CGHUB_SERVER = 'https://192.35.223.223'
CGHUB_SERVER_SOLR_URI = '/solr/select/'
# CGHUB_SERVER = 'http://127.0.0.1:8983'
API_HTTP_ERROR_ATTEMPTS = 5
API_HTTP_ERROR_SLEEP_AFTER = 1
API_TYPE = 'WSAPI'
