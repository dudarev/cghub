# -*- coding: utf-8 -*-
"""
cghub_api.utils
~~~~~~~~~~~~~~~~~~~~

Utility functions.

"""
import os
import datetime

from settings import CACHE_DIR


def clear_cache(older_than):
    """
    Clear cache older that some time.

    :param older_than: datetime object older which cache files are deleted.
    """
    for dirpath, dirnames, filenames in os.walk(CACHE_DIR):
        for f in filenames:
            if datetime.datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(CACHE_DIR,f))
                    ) < older_than:
                os.remove(os.path.join(CACHE_DIR,f))
    pass
