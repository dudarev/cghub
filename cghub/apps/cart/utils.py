import sys
import csv
import urllib2

from StringIO import StringIO
from lxml import etree, objectify

from celery import states
from djcelery.models import TaskState

from django.http import HttpResponse
from django.core.servers import basehttp
from django.conf import settings
from django.utils import timezone

from cghub.wsapi.api import Results
from cghub.wsapi.api import request as api_request

from cghub.apps.core.templatetags.search_tags import field_values
from cghub.apps.core.utils import (get_wsapi_settings, get_wsapi_settings,
                                            generate_task_id)
from cghub.apps.core.attributes import ATTRIBUTES

from cghub.apps.cart.tasks import cache_results_task
from cghub.apps.cart.cache import AnalysisFileException, get_analysis


WSAPI_SETTINGS = get_wsapi_settings()


def get_or_create_cart(request):
    """ return cart and creates it if it does not exist """
    request.session["cart"] = request.session.get('cart', {})
    return request.session["cart"]


def add_file_to_cart(request, file_dict):
    """ adds file file_dict to cart """
    cart = get_or_create_cart(request)
    analysis_id = file_dict.get('analysis_id')
    if analysis_id not in cart:
        cart[analysis_id] = file_dict
    request.session.modified = True


def remove_file_from_cart(request, analysis_id):
    """ removes file with legacy_sample_id from cart """
    cart = get_or_create_cart(request)
    if analysis_id in cart:
        del cart[analysis_id]
    request.session.modified = True


def get_cart_stats(request):
    cart = get_or_create_cart(request)
    stats = {'count': len(cart), 'size': 0}
    for analysis_id, f in cart.iteritems():
        if 'files_size' in f and isinstance(f['files_size'], (int, long)):
            stats['size'] += f['files_size']
    return stats


def add_ids_to_cart(request, ids):
    """ adds file file_dict to cart """
    cart = get_or_create_cart(request)
    for i in ids:
        if i not in cart:
            cart[i] = {'analysis_id': i}
    request.session.modified = True


def clear_cart(request):
    if 'cart' in request.session:
        request.session['cart'].clear()
    request.session['cart_loading'] = False
    request.session.modified = True


def check_missing_files(files):
    """
    Check that not only analysis_id attribute filled.
    If only analysis_id exists, upload missing attributes and modify data

    :param files: list of files attributes
    """
    files_to_upload = []
    for f in files:
        if len(f) == 1:
            files_to_upload.append(f['analysis_id'])
    if files_to_upload:
        query = 'analysis_id=' + urllib2.quote('(%s)' % ' OR '.join(files_to_upload))
        result = api_request(
            query=query,
            ignore_cache=True,
            use_api_light=False,
            settings=WSAPI_SETTINGS)
        if hasattr(result, 'Result'):
            result.add_custom_fields()
            for i in result.Result:
                for f in files:
                    if f['analysis_id'] == i.analysis_id:
                        for attr in ATTRIBUTES:
                            f[attr] = getattr(i, attr)
                        break
    return files


def cache_file(analysis_id, last_modified, asinc=False):
    """
    Create celery task if asinc==True, or execute task function.
    Previously check that task was not created yet.
    """
    if not asinc:
        cache_results_task(analysis_id, last_modified)
        return
    task_id = generate_task_id(analysis_id=analysis_id, last_modified=last_modified)
    try:
        task = TaskState.objects.get(task_id=task_id)
        # task failed, reexecute task
        if task.state == states.FAILURE:
            # restart
            cache_results_task.apply_async(
                    kwargs={
                        'analysis_id': analysis_id,
                        'last_modified': last_modified},
                    task_id=task_id)
    except TaskState.DoesNotExist:
        # run
        cache_results_task.apply_async(
                    kwargs={
                        'analysis_id': analysis_id,
                        'last_modified': last_modified},
                    task_id=task_id)


def join_analysises(data, short=False, live_only=False):
    """
    Join xml files with specified ids.
    If file exists in cache, it will be used, otherwise, file will be downloaded and saved to cache.

    :param data: cart data like it stored in session: {analysis_id: {'last_modified': '..', 'state': '..', ...}, analysis_id: {..}, ...}
    :param short: if True - file will be contains only most necessary attributes
    :param live_only: if True - files with state attribute != 'live' will be not included to results
    """
    results = None
    results_counter = 1
    for analysis_id in data:
        if live_only and data[analysis_id].get('state') != 'live':
            continue
        last_modified = data[analysis_id].get('last_modified')
        try:
            result = get_analysis(analysis_id, last_modified, short=short)
        except AnalysisFileException:
            continue
        if results is None:
            results = result
            results.Query.clear()
            results.Hits.clear()
        else:
            result.Result.set('id', u'{0}'.format(results_counter))
            # '+ 1' because the first two elements (0th and 1st) are Query and Hits
            results.insert(results_counter + 1, result.Result)
        results_counter += 1
    if results:
        return results
    return _empty_results()


def manifest(data):
    results = join_analysises(data, live_only=True, short=True)
    mfio = _stream_with_xml(results)
    response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=manifest.xml'
    return response


def metadata(data):
    results = join_analysises(data)
    mfio = _stream_with_xml(results)
    response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response


def summary(data):
    results = join_analysises(data)
    results.add_custom_fields()
    mfio = _write_summary_tsv(results)
    response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/tsv')
    response['Content-Disposition'] = 'attachment; filename=summary.tsv'
    return response


def _empty_results():
    results = Results(
        objectify.fromstring('<ResultSet></ResultSet>'),
        settings=get_wsapi_settings())
    results.set('date', timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    results.insert(0, objectify.fromstring('<Query></Query>'))
    results.insert(1, objectify.fromstring('<Hits></Hits>'))
    results.insert(2, objectify.fromstring(
        '<ResultSummary>'
        '<downloadable_file_count>0</downloadable_file_count>'
        '<downloadable_file_size units="GB">0</downloadable_file_size>'
        '<state_count>'
        '<live>0</live>'
        '</state_count>'
        '</ResultSummary>'))
    return results


def _stream_with_xml(results):
    stringio = StringIO()
    parser = etree.XMLParser()
    tree = etree.XML(results.tostring(), parser)
    stringio.write(etree.tostring(tree, pretty_print=True))
    stringio.seek(0)
    return stringio


def _write_summary_tsv(results):
    stringio = StringIO()
    csvwriter = csv.writer(stringio, quoting=csv.QUOTE_MINIMAL, dialect='excel-tab')

    csvwriter.writerow([field.lower().replace(' ', '_')
                        for field in settings.TABLE_COLUMNS])
    for result in results.Result:
        fields = field_values(result)

        row = []
        for field_name in settings.TABLE_COLUMNS:
            value = fields.get(field_name, None)
            if value is None:
                continue
            row.append(value)
        csvwriter.writerow(row)

    stringio.seek(0)
    return stringio
