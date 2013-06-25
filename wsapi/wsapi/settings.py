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
    :param HTTP_ERROR_ATTEMPTS: number of attempts to connect to server after HTTP503 was raised
    :param HTTP_ERROR_SLEEP_AFTER: number of seconds to wait before next attempt to connect to server after HTTP503 was raised

"""

SETTINGS_DEFAULT = dict(
    CGHUB_SERVER='https://stage.cghub.ucsc.edu/',
    CGHUB_ANALYSIS_ID_URI='/cghub/metadata/analysisId',
    CGHUB_ANALYSIS_DETAIL_URI='/cghub/metadata/analysisDetail',
    CGHUB_ANALYSIS_FULL_URI='/cghub/metadata/analysisFull',
    HTTP_ERROR_ATTEMPTS=5,
    HTTP_ERROR_SLEEP_AFTER=1,
)
