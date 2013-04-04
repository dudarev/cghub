import glob
import datetime
import os

from django.conf import settings
from django.utils.http import urlquote
from celery.task import task

from cghub.apps.cart.cache import AnalysisFileException, save_to_cart_cache
from cghub.apps.core.utils import get_filters_string
from cghub.apps.cart.parsers import parse_cart_attributes

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore


@task(ignore_result=True)
def cache_results_task(analysis_id, last_modified):
    """
    If file for specified uid not exists in settings.CART_CACHE_DIR,
    attributes will be received and saved.
    Two different files will be saved,
    the first contains all attributes and the second only most necessary ones.

    :param analysis_id: file analysis id
    :param last_modified: file last_modified
    """
    try:
        save_to_cart_cache(analysis_id, last_modified)
    except AnalysisFileException:
        pass


@task(ignore_result=True)
def add_files_to_cart_by_query_task(data, session_key):
    """
    Obtains all results for specified query and adds them to cart

    :param data: AllFilesForm form cleaned data: ``{'attributes': [...], 'filters': {...}}``
    :param session_key: Session.session_key

    How to change variables stored in session:
    https://docs.djangoproject.com/en/dev/topics/http/sessions/#using-sessions-out-of-views
    """
    # check session exists
    try:
         Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        return
    # modify session
    s = SessionStore(session_key=session_key)
    cart = s.get('cart', {})
    attributes = data['attributes']
    filters = data['filters']
    filter_str = get_filters_string(filters)
    q = filters.get('q')
    if q:
        query = u"xml_text={0}".format(urlquote(q))
        query += filter_str
    else:
        query = filter_str[1:]  # remove front ampersand
    if 'xml_text' in query:
        parse_cart_attributes(s, attributes, query=query)
        parse_cart_attributes(s, attributes,
                    query=query.replace('xml_text', 'analysis_id', 1))
    else:
        parse_cart_attributes(s, attributes, query=query)


# FIXME(nanvel): now cache stored in folders
'''
@task(ignore_result=True)
def cache_clear_task():
    """
    Removes files from settings.CART_CACHE_DIR which are older than
    settings.TIME_DELETE_CART_CACHE_FILES_OLDER
    """
    files = glob.glob(os.path.join(settings.CART_CACHE_DIR, '*'))
    now = datetime.datetime.now()
    for file in files:
        time_file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        if now - time_file_modified > settings.TIME_DELETE_CART_CACHE_FILES_OLDER:
            os.remove(file)
'''
