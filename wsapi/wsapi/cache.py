# -*- coding: utf-8 -*-
"""
wsapi.cache
~~~~~~~~~~~~~~~~~~~~

Module contains functions for work with cache.

"""

import os
import hashlib
import urllib2

from lxml import objectify, etree

from exceptions import QueryRequired

from utils import get_setting


_backends = ('simple', )

def _dummy_get_from_cache(**kwargs):
    """Does nothing, imitates reading from the cache"""
    return ([], ())

def _dummy_save_to_cache(**kwargs):
    """Does nothing, imitates reading from the cache"""
    pass

def get_cache_file_name(query, get_attributes, full, settings):
    # Prevent getting different file names because of 
    # percent escaping
    query = urllib2.unquote(query.encode("utf8"))
    query = urllib2.quote(query)
    md5 = hashlib.md5(query)
    if get_attributes:
        if full:
            cache_file_name = u'{0}_full.xml'.format(md5.hexdigest())
        else:
            cache_file_name = u'{0}.xml'.format(md5.hexdigest())
    else:
        cache_file_name = u'{0}_short.xml'.format(md5.hexdigest())

    cache_file_name = os.path.join(
                get_setting('CACHE_DIR', settings),
                cache_file_name)

    return cache_file_name

def _get_from_simple_cache(settings, query=None, get_attributes=True, full=False):
    """Reads from the cache file, which name is calculating from query"""
    results = []
    errors = []

    if not query:
        raise QueryRequired

    cache_file_name = get_cache_file_name(
                        query=query,
                        get_attributes=get_attributes,
                        full=full,
                        settings=settings)

    # getting results from cache file
    if os.path.exists(cache_file_name):
        try:
            results = objectify.fromstring(open(cache_file_name, 'r').read())
        except etree.XMLSyntaxError as e:
            errors.append(e)

    return (results, tuple(errors))

def _save_to_simple_cache(settings, query=None, get_attributes=True,
                                                full=False, data=None):
    """Writes related to the query data into the cache file, which creates if necessary"""
    if not query:
        return

    cache_file_name = get_cache_file_name(
                    query=query,
                    get_attributes=get_attributes,
                    full=full,
                    settings=settings)
    cache_dir = get_setting('CACHE_DIR', settings)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    with open(cache_file_name, 'w') as f:
        f.write(data.tostring())


# Determinating which functions to use depending on settings
# Dummy functions are for defalt
get_from_cache = _dummy_get_from_cache
save_to_cache = _dummy_save_to_cache

if not get_setting('USE_CACHE') or not get_setting('CACHE_BACKEND') in _backends:
    get_from_cache = _dummy_get_from_cache
    save_to_cache = _dummy_save_to_cache
elif get_setting('CACHE_BACKEND') == 'simple':
    get_from_cache = _get_from_simple_cache
    save_to_cache = _save_to_simple_cache
