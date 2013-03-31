import glob
import datetime
import os

from django.conf import settings
from django.utils import timezone
from celery.task import task

from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import multiple_request as api_multiple_request
from cghub.apps.cart.cache import (AnalysisFileException, save_to_cart_cache,
                                                    is_cart_cache_exists)
from cghub.apps.core.utils import (get_wsapi_settings, get_filters_string,
                                                        is_celery_alive)

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore


WSAPI_SETTINGS = get_wsapi_settings()


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
    celery_alive = is_celery_alive()
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
        queries_list = [query, query.replace('xml_text', 'analysis_id', 1)]
        results = api_multiple_request(queries_list=queries_list,
                                            settings=WSAPI_SETTINGS)
    else:
        results = api_request(query=query, settings=WSAPI_SETTINGS)
    results.add_custom_fields()
    if hasattr(results, 'Result'):
        for r in results.Result:
            r_attrs = dict(
                (attr, unicode(getattr(r, attr)))
                for attr in attributes if hasattr(r, attr))
            analysis_id = unicode(r.analysis_id)
            r_attrs['files_size'] = int(r.files_size)
            r_attrs['analysis_id'] = analysis_id
            if analysis_id not in cart:
                cart[analysis_id] = r_attrs
                last_modified = r_attrs['last_modified']
                if not is_cart_cache_exists(analysis_id, last_modified):
                    if celery_alive:
                        cache_results_task.delay(analysis_id, last_modified)
                    else:
                        cache_results_task(analysis_id, last_modified)
    s['cart'] = cart
    s.save()


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
