import glob
import datetime
import os

from django.conf import settings
from django.utils import timezone
from celery.task import task
from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import multiple_request as api_multiple_request
from cghub.apps.core.utils import get_wsapi_settings, get_filters_string

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore


WSAPI_SETTINGS = get_wsapi_settings()


@task(ignore_result=True)
def cache_results_task(file_dict):
    analysis_id = file_dict.get('analysis_id')
    filename_with_attributes = os.path.join(settings.CART_CACHE_DIR,
        "{0}_with_attributes".format(analysis_id))
    filename_without_attributes = os.path.join(settings.CART_CACHE_DIR,
        "{0}_without_attributes".format(analysis_id))
    if os.path.isfile(filename_with_attributes) and os.path.isfile(filename_without_attributes):
        return
    result = api_request(
                query='analysis_id={0}'.format(analysis_id),
                settings=WSAPI_SETTINGS)
    with open(filename_with_attributes, 'w') as f:
        f.write(result.tostring())
    with open(filename_without_attributes, 'w') as f:
        result.remove_attributes()
        f.write(result.tostring())


@task(ignore_result=True)
def add_files_to_cart_by_query(data, session_key):
    """
    Obtain all results for specified query and add them to cart

    data - AllFilesForm form cleaned data:
    {'attributes': [...], 'filters': {...}}
    session_key - Session.session_key

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
    cart = s.get('cart', None)
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
    s['cart'] = cart
    s.save()


@task(ignore_result=True)
def cache_clear_task():
    files = glob.glob(os.path.join(settings.CART_CACHE_DIR, '*'))
    now = timezone.now()
    for file in files:
        time_file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        if now - time_file_modified > settings.TIME_DELETE_CART_CACHE_FILES_OLDER:
            os.remove(file)
