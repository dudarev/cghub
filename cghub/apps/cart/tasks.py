import glob
import datetime
import os

from django.conf import settings
from celery.task import task

from cghub.apps.cart.cache import AnalysisFileException, save_to_cart_cache
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
def add_files_to_cart_by_query_task(queries, attributes, session_key):
    """
    Obtains all results for specified query and adds them to cart

    :param queries: list of queries data should be obtained by
    :param attributes: list of attributes should be added to cart
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
    session_store = SessionStore(session_key=session_key)
    for query in queries:
        parse_cart_attributes(session_store, attributes, query=query)
    session_store['cart_loading'] = False
    session_store.save()


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
