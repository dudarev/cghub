import csv
import datetime
import logging

from StringIO import StringIO

from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.db.models import Sum

from cghub.apps.core.templatetags.search_tags import field_values
from cghub.apps.core.utils import xml_add_spaces

from .cache import AnalysisFileException, get_analysis, get_analysis_xml
from .models import CartItem, Analysis


cart_logger = logging.getLogger('cart')


def update_analysis(analysis_id):
    pass


class Cart(object):

    def __init__(self, session):
        if session.session_key == None:
            session.save()
        session_object = Session.objects.get(session_key=session.session_key)
        self.cart = session_object.cart

    @property
    def size(self):
        return self.cart.size

    @property
    def all_count(self):
        return self.cart.items.count()

    @property
    def live_count(self):
        return self.cart.live_count

    def remove(self, analysis_id):
        try:
            item = CartItem.objects.get(
                        cart=self.cart, analysis__analysis_id=analysis_id)
        except CartItem.DoesNotExist:
            return
        item.delete()

    def add(self, result):
        analysis_id = result['analysis_id']
        try:
            analysis = Analysis.objects.get(analysis_id=analysis_id)
            if analysis.last_modified != result['last_modified']:
                update_analysis(analysis_id)
            item = CartItem(
                    cart=self.cart,
                    analysis=analysis)
            item.save()
        except IntegrityError:
            return
        except Analysis.DoesNotExist:
            analysis = update_analysis(analysis_id)
            item = CartItem(
                    cart=self.cart,
                    analysis=analysis)
            item.save()

    def clear(self):
        pass

    def update_stats(self):
        """
        Update cart.size and cart.live_count
        """
        items = self.cart.items
        self.cart.size = items.aggregate(
                size=Sum('analysis__files_size'))['size']
        self.cart.live_count = items.filter(analysis__state='live').count()
        self.cart.save()


def get_or_create_cart(request):
    """ return cart and creates it if it does not exist """
    request.session["cart"] = request.session.get('cart', {})
    return request.session["cart"]


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


def cart_clear(request):
    if 'cart' in request.session:
        request.session['cart'].clear()
    request.session.modified = True


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
