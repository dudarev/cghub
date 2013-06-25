# -*- coding: utf-8 -*-
"""
wsapi.utils
~~~~~~~~~~~~~~~~~~~~

Utility functions.

"""

import urllib2
import time

from .settings import SETTINGS_DEFAULT


ALLOWED_SORT_BY = ('aliquot_id', 'analysis_id', 'analyte_code', 'center_name',
    'disease_abbr', 'last_modified', 'legacy_sample_id',
    'library_strategy', 'participant_id', 'platform', 'published_date',
    'refassem_short_name', 'sample_accession', 'sample_id', 'sample_type',
    'state', 'study', 'tss_id', 'upload_date')

FORMAT_CHOICES = {
    'xml': 'text/xml',
    'json': 'application/json'
}


def get_setting(attribute, settings={}):
    return settings.get(attribute) or SETTINGS_DEFAULT.get(attribute)


def urlopen(url, format='xml', settings={}):
    """
    Retry to get answer from CGHUB server if HTTP503 raised.
    Maximum attempts == HTTP_ERROR_ATTEMPTS.
    Time delay between attempts == HTTP_ERROR_SLEEP_AFTER.

    :param url: url
    :param format: 'xml' or 'json'
    :param settings: custom settings, see `wsapi.settings.py` for settings example
    """
    http_error_attempts = get_setting('HTTP_ERROR_ATTEMPTS', settings)
    http_error_sleep_after = get_setting('HTTP_ERROR_SLEEP_AFTER', settings)
    headers = {'Accept': FORMAT_CHOICES.get(format, FORMAT_CHOICES['xml'])}
    for i in range(http_error_attempts):
        try:
            req = urllib2.Request(url, headers=headers)
            return urllib2.urlopen(req)
        except urllib2.URLError:
            time.sleep(HTTP_ERROR_SLEEP_AFTER)
    raise urllib2.URLError('No response after %d attempts' % HTTP_ERROR_ATTEMPTS)


def prepare_query(query, offset=None, limit=None, sort_by=None):
    """
    Quote all values in query and adds start, rows and sort_by if necessary.

    :param :
    """
    if query is None:
        return query
    query = urllib2.unquote(query)
    parts = []
    for part in query.split('&'):
        try:
            attr, val = part.split('=')
            if attr not in ('limit', 'offset', 'sort_by'):
                parts.append('='.join([attr, urllib2.quote(val)]))
        except ValueError:
            parts.append(part)
    if offset:
        parts.append('='.join(['start', urllib2.quote(str(offset))]))
    if limit:
        parts.append('='.join(['rows', urllib2.quote(str(limit))]))
    if sort_by and (sort_by in ALLOWED_SORT_BY or sort_by[1:] in ALLOWED_SORT_BY):
        if sort_by[0] == '-':
            parts.append('='.join(['sort_by', '%s:desc' % urllib2.quote(sort_by[1:])]))
        else:
            parts.append('='.join(['sort_by', '%s:asc' % urllib2.quote(sort_by)]))
    return '&'.join(parts)
