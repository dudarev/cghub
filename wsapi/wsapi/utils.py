# -*- coding: utf-8 -*-
"""
wsapi.utils
~~~~~~~~~~~~~~~~~~~~

Utility functions.

"""
import os
import datetime

from settings import SETTINGS_DEFAULT


def get_setting(attribute, settings={}):
    return settings.get(attribute) or SETTINGS_DEFAULT.get(attribute)

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
