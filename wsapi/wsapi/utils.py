# -*- coding: utf-8 -*-
"""
wsapi.utils
~~~~~~~~~~~~~~~~~~~~

Utility functions.

"""
import os
import datetime
import urllib2
import time

from settings import SETTINGS_DEFAULT


def get_setting(attribute, settings={}):
    return settings.get(attribute) or SETTINGS_DEFAULT.get(attribute)


HTTP_ERROR_ATTEMPTS = get_setting('HTTP_ERROR_ATTEMPTS')
HTTP_ERROR_SLEEP_AFTER = get_setting('HTTP_ERROR_SLEEP_AFTER')


def urlopen(url):
    """
    Retry to get answer from CGHUB server if HTTP503 raised.
    Maximum attempts == HTTP_ERROR_ATTEMPTS.
    Time delay between attempts == HTTP_ERROR_SLEEP_AFTER.
    """
    for i in range(HTTP_ERROR_ATTEMPTS):
        try:
            req = urllib2.Request(url)
            return urllib2.urlopen(req)
        except urllib2.URLError:
            time.sleep(HTTP_ERROR_SLEEP_AFTER)
    raise urllib2.URLError


def clear_cache(cache_dir, older_than):
    """
    Clear cache older that some time.

    :param cache_dir: path to directory where cache files located
    :param older_than: datetime object older which cache files are deleted.
    """
    for dirpath, dirnames, filenames in os.walk(cache_dir):
        for f in filenames:
            if datetime.datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(cache_dir,f))
                    ) < older_than:
                os.remove(os.path.join(cache_dir,f))
    pass
