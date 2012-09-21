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
from settings import (USE_CACHE, CACHE_BACKEND, CACHE_DIR)


_backends = ('simple', )

def _dummy_get_from_cache(**kwargs):
    """Does nothing, imitates reading from the cache"""
    return ([], ())

def _dummy_save_to_cache(**kwargs):
    """Does nothing, imitates reading from the cache"""
    pass

def get_cache_file_name(query, get_attributes):
    # Prevent getting different file names because of 
    # percent escaping
    query = urllib2.unquote(query.encode("utf8"))
    query = urllib2.quote(query)
    md5 = hashlib.md5(query)
    cache_file_name = u'{0}.xml'.format(md5.hexdigest())
    if not get_attributes:
        cache_file_name = cache_file_name + '-no-attr'
    cache_file_name = os.path.join(CACHE_DIR, cache_file_name)

    return cache_file_name

def _get_from_simple_cache(query=None, get_attributes=True):
    """Reads from the cache file, which name is calculating from query"""
    results = []
    errors = []

    if not query:
        raise QueryRequired

    cache_file_name = get_cache_file_name(query=query, get_attributes=get_attributes)
    print cache_file_name
    # getting results from cache file
    if os.path.exists(cache_file_name):
        try:
            results = objectify.fromstring(open(cache_file_name, 'r').read())
        except etree.XMLSyntaxError as e:
            errors.append(e)

    return (results, tuple(errors))

def _save_to_simple_cache(query=None, get_attributes=True, data=None):
    """Writes related to the query data into the cache file, which creates if necessary"""
    if not query:
        return

    cache_file_name = get_cache_file_name(query=query, get_attributes=get_attributes)

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    with open(cache_file_name, 'w') as f:
        f.write(data.tostring())


# Determinating which functions to use depending on settings
# Dummy functions are for defalt
get_from_cache = _dummy_get_from_cache
save_to_cache = _dummy_save_to_cache

if not USE_CACHE or not CACHE_BACKEND in _backends:
    get_from_cache = _dummy_get_from_cache
    save_to_cache = _dummy_save_to_cache
elif CACHE_BACKEND == 'simple':
    get_from_cache = _get_from_simple_cache
    save_to_cache = _save_to_simple_cache