import os
import hashlib

from lxml import objectify, etree

from exceptions import QueryRequired
from settings import (USE_CACHE, CACHE_BACKEND, CACHE_DIR)


_backends = ('simple', )

def _dummy_get_from_cache(**kwargs):
    return ([], ())

def _dummy_save_to_cache(**kwargs):
    pass

def _get_from_simple_cache(query=None, get_attributes=True):
    results = []
    errors = []

    if not query:
        raise QueryRequired

    # geting cache file's name
    md5 = hashlib.md5(query)
    cache_file_name = u'{0}.xml'.format(md5.hexdigest())
    if not get_attributes:
        cache_file_name = cache_file_name + '-no-attr'
    cache_file_name = os.path.join(CACHE_DIR, cache_file_name)

    # getting results from cache file
    if os.path.exists(cache_file_name):
        try:
            results = objectify.fromstring(open(cache_file_name, 'r').read())
        except etree.XMLSyntaxError as e:
            errors.append(e)

    return (results, tuple(errors))

def _save_to_simple_cache(query=None, data=None):
    if not query:
        return

    md5 = hashlib.md5(query)
    cache_file_name = u'{0}.xml'.format(md5.hexdigest())

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    with open(cache_file_name, 'w') as f:
        f.write(data.tostring())


if not USE_CACHE or not CACHE_BACKEND in _backends:
    get_from_cache = _dummy_get_from_cache
    save_to_cache = _dummy_save_to_cache
elif CACHE_BACKEND == 'simple':
    get_from_cache = _get_from_simple_cache
    save_to_cache = _save_to_simple_cache