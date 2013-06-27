import sys
import csv
import urllib2
import datetime
import logging

from StringIO import StringIO

from cghub.wsapi import request_page

from django.http import HttpResponse
from django.core.servers import basehttp
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string, get_template
from django.template import Context

from cghub.apps.core.templatetags.search_tags import field_values
from cghub.apps.core.utils import (get_wsapi_settings, get_wsapi_settings,
                                        generate_task_id, xml_add_spaces)
from cghub.apps.core.attributes import ATTRIBUTES

from cghub.apps.cart.cache import (AnalysisFileException, get_analysis,
                                                        get_analysis_xml)


WSAPI_SETTINGS = get_wsapi_settings()
cart_logger = logging.getLogger('cart')


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
        if 'files_size' in f:
            try:
                size = int(f['files_size'])
            except TypeError, ValueError:
                size = 0
            stats['size'] += size
    return stats


def add_ids_to_cart(request, ids):
    """ adds file file_dict to cart """
    cart = get_or_create_cart(request)
    for i in ids:
        if i not in cart:
            cart[i] = {'analysis_id': i}
    request.session.modified = True


def add_files_to_cart(request, results):
    """
    Fill cart by data contains in results.

    :param request: Request objects
    :param results: attributes dict
    """
    if len(results) == 0:
        return
    cart = get_or_create_cart(request)
    for result in results:
        current_dict = {}
        for attribute in ATTRIBUTES:
            current_dict[attribute] = result[attribute]
        cart[current_dict['analysis_id']] = current_dict
    request.session.modified = True


def cart_clear(request):
    if 'cart' in request.session:
        request.session['cart'].clear()
    request.session.modified = True


def cart_remove_files_without_attributes(request):
    """
    Remove files from cart where last_modified not specified.
    Return number of removed files.
    """
    cart = get_or_create_cart(request)
    to_remove = []
    for analysis_id, f in cart.iteritems():
        if 'last_modified' not in f:
            to_remove.append(analysis_id)
    for analysis_id in to_remove:
        del cart[analysis_id]
    if to_remove:
        request.session.modified = True
    return len(to_remove)


def load_missing_attributes(files):
    """
    Check that not only analysis_id attribute filled.
    If only analysis_id exists, upload missing attributes and modify data.

    Runs only if task to fill attributes in progress.

    :param files: list of files attributes
    """
    files_to_upload = []
    for f in files:
        if len(f) == 1:
            files_to_upload.append(f['analysis_id'])
    if files_to_upload:
        query = 'analysis_id=' + urllib2.quote('(%s)' % ' OR '.join(files_to_upload))
        hits, results = request_page(query=query, settings=WSAPI_SETTINGS)
        if hits != 0:
            for result in results:
                for f in files:
                    if f['analysis_id'] == result['analysis_id']:
                        for attr in ATTRIBUTES:
                            f[attr] = result.get(attr)
                        break
    return files


def analysis_xml_iterator(data, short=False, live_only=False):
    """
    Return xml for files with specified ids.
    If file exists in cache, it will be used, otherwise, file will be downloaded and saved to cache.

    :param data: cart data like it stored in session: {analysis_id: {'last_modified': '..', 'state': '..', ...}, analysis_id: {..}, ...}
    :param short: if True - file will be contains only most necessary attributes
    :param live_only: if True - files with state attribute != 'live' will be not included to results
    """
    yield render_to_string('xml/analysis_xml_header.xml', {
                        'date': datetime.datetime.strftime(
                                    timezone.now(), '%Y-%d-%m %H:%M:%S'),
                        'len': len(data)})
    counter = 0
    downloadable_size = 0
    result_template = get_template('xml/analysis_xml_result.xml')
    for f in data:
        if live_only and data[f].get('state') != 'live':
            continue
        last_modified = data[f].get('last_modified')
        try:
            xml, files_size = get_analysis_xml(
                            analysis_id=f,
                            last_modified=last_modified,
                            short=short)
        except AnalysisFileException as e:
            cart_logger.error('Error while composing metadata xml. %s' % str(e))
            continue
        counter += 1
        downloadable_size += files_size
        formatted_xml = ''
        for s in xml_add_spaces(xml, space=4, tab=2):
            formatted_xml += s
        yield result_template.render(Context({
                    'counter': counter,
                    'xml': formatted_xml.strip()}))
    yield render_to_string('xml/analysis_xml_summary.xml', {
                    'counter': counter,
                    'size': str(round(downloadable_size/1073741824.*100)/100)})


def summary_tsv_iterator(data):
    """
    Returns Summary tsv file content.
    Data to generate file takes from cart cache. If data not exists in cache,
    it will be downloaded.

    param data: cart data like it stored in session: {analysis_id: {'last_modified': '..', 'state': '..', ...}, analysis_id: {..}, ...}
    """
    COLUMNS = settings.TABLE_COLUMNS
    stringio = StringIO()
    csvwriter = csv.writer(stringio, quoting=csv.QUOTE_MINIMAL, dialect='excel-tab', lineterminator='\n')
    csvwriter.writerow([field.lower().replace(' ', '_') for field in COLUMNS])
    for f in data:
        last_modified = data[f].get('last_modified')
        try:
            result = get_analysis(
                            analysis_id=f,
                            last_modified=last_modified)
        except AnalysisFileException as e:
            cart_logger.error('Error while composing summary tsv. %s' % str(e))
            continue
        fields = field_values(result, humanize_files_size=False)
        row = []
        for field_name in COLUMNS:
            value = fields.get(field_name, None)
            row.append(value or '')
        csvwriter.writerow(row)
        stringio.seek(0)
        line = stringio.read()
        stringio.seek(0)
        stringio.truncate()
        yield line


def manifest(data):
    response = HttpResponse(
            analysis_xml_iterator(data, short=True, live_only=True),
            content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=manifest.xml'
    return response


def metadata(data):
    response = HttpResponse(analysis_xml_iterator(data), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response


def summary(data):
    response = HttpResponse(summary_tsv_iterator(data), content_type='text/tsv')
    response['Content-Disposition'] = 'attachment; filename=summary.tsv'
    return response
