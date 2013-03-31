import sys
import csv

from StringIO import StringIO
from lxml import etree, objectify

from django.http import HttpResponse
from django.core.servers import basehttp
from django.conf import settings
from django.utils import timezone

from cghub.wsapi.api import Results

from cghub.apps.core.templatetags.search_tags import field_values
from cghub.apps.core.utils import get_wsapi_settings
from cghub.apps.cart.tasks import cache_results_task
from cghub.apps.cart.cache import AnalysisFileException, get_analysis


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


def clear_cart(request):
    if 'cart' in request.session:
        request.session['cart'].clear()
        request.session.modified = True


def cache_results(file_dict):
    """
    To check celery status use cghub.apps.core.utils.py:is_celery_alive
    """
    try:
        cache_results_task.delay(file_dict)
    except:
        cache_results_task(file_dict)


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
                        for field, visibility in settings.TABLE_COLUMNS])
    for result in results.Result:
        fields = field_values(result)

        row = []
        for field_name, default_state in settings.TABLE_COLUMNS:
            value = fields.get(field_name, None)
            if value == None:
                continue
            row.append(value)
        csvwriter.writerow(row)

    stringio.seek(0)
    return stringio
