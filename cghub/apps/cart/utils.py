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
from cghub.apps.core.utils import xml_add_spaces, RequestDetail

from .cache import AnalysisException, get_analysis, get_analysis_xml
from .models import CartItem, Analysis


cart_logger = logging.getLogger('cart')


class Cart(object):
    """
    Class allows to manage user cart.
    """

    def __init__(self, session):
        if session.session_key == None:
            session.save()
        session_object = Session.objects.get(session_key=session.session_key)
        self.session = session
        self.cart = session_object.cart

    @property
    def size(self):
        """
        Returns size of all items in cart.
        """
        return self.cart.size

    @property
    def all_count(self):
        return self.cart.items.count()

    @property
    def live_count(self):
        """
        Returns count of cart items with state == 'live'
        """
        return self.cart.live_count

    def remove(self, analysis_id):
        try:
            item = CartItem.objects.get(
                        cart=self.cart, analysis__analysis_id=analysis_id)
        except CartItem.DoesNotExist:
            return
        item.delete()

    def page(self, offset=0, limit=10):
        items = self.cart.items.all()[offset * limit:(offset + 1) * limit]
        if not items.exists():
            return []
        results = []
        api_request = RequestDetail(query={
                'analysis_id': [i.analysis.analysis_id for i in items]})
        cart_data = {}
        for i in items:
            analysis = i.analysis
            cart_data[analysis.analysis_id] = {
                    'last_modified': analysis.last_modified, 'state': analysis.state}
        for result in api_request.call():
            # replace last_modified and state to that specified in Analysis
            analysis_id = result['analysis_id']
            result['last_modified'] = cart_data[analysis_id]['last_modified']
            result['state'] = cart_data[analysis_id]['state']
            results.append(result)
        return results

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
            analysis = Analysis.objects.create(
                    analysis_id=analysis_id,
                    last_modified=result['last_modified'],
                    state=result['state'],
                    files_size=result['files_size'])
            item = CartItem(
                    cart=self.cart,
                    analysis=analysis)
            item.save()

    def clear(self):
        self.cart.items.all().delete()
        self.update_stats()

    def update_stats(self):
        """
        Update cart.size and cart.live_count
        """
        items = self.cart.items
        self.cart.size = items.aggregate(
                size=Sum('analysis__files_size'))['size'] or 0
        self.cart.live_count = items.filter(analysis__state='live').count()
        self.cart.save()
        self.session['cart_count'] = self.cart.live_count


def analysis_xml_iterator(cart, short=False, live_only=False):
    """
    Return xml for files with specified ids.
    If file exists in cache, it will be used, otherwise, file will be downloaded and saved to cache.

    :param data: cart data like it stored in session: {analysis_id: {'last_modified': '..', 'state': '..', ...}, analysis_id: {..}, ...}
    :param short: if True - file will be contains only most necessary attributes
    :param live_only: if True - files with state attribute != 'live' will be not included to results
    """
    if live_only:
        items = cart.cart.items.filter(analysis__state='live')
    else:
        items = cart.cart.items.all()
    yield render_to_string('xml/analysis_xml_header.xml', {
                        'date': datetime.datetime.strftime(
                                    timezone.now(), '%Y-%d-%m %H:%M:%S'),
                        'len': items.count()})
    counter = 0
    downloadable_size = 0
    result_template = get_template('xml/analysis_xml_result.xml')
    for item in items:
        analysis = item.analysis
        try:
            xml, files_size = get_analysis_xml(
                            analysis_id=analysis.analysis_id,
                            last_modified=analysis.last_modified,
                            short=short)
        except AnalysisException as e:
            cart_logger.error('Error while composing metadata xml. %s' % str(e))
            continue
        counter += 1
        downloadable_size += analysis.files_size
        formatted_xml = ''
        for s in xml_add_spaces(xml, space=4, tab=2):
            formatted_xml += s
        yield result_template.render(Context({
                    'counter': counter,
                    'xml': formatted_xml.strip()}))
    yield render_to_string('xml/analysis_xml_summary.xml', {
                    'counter': counter,
                    'size': str(round(downloadable_size / 1073741824. * 100) / 100)})


def summary_tsv_iterator(cart):
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
    items = cart.cart.items.all()
    for item in items:
        analysis = item.analysis
        try:
            result = get_analysis(
                            analysis_id=analysis.analysis_id,
                            last_modified=analysis.last_modified)
        except AnalysisException as e:
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


def manifest(cart):
    response = HttpResponse(
            analysis_xml_iterator(cart, short=True, live_only=True),
            content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=manifest.xml'
    return response


def metadata(cart):
    response = HttpResponse(analysis_xml_iterator(cart), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response


def summary(cart):
    response = HttpResponse(summary_tsv_iterator(cart), content_type='text/tsv')
    response['Content-Disposition'] = 'attachment; filename=summary.tsv'
    return response


def item_metadata(analysis_id, last_modified):
    content = render_to_string('xml/analysis_xml_header.xml', {
                        'date': datetime.datetime.strftime(
                                    timezone.now(), '%Y-%d-%m %H:%M:%S'),
                        'len': 1})
    result_template = get_template('xml/analysis_xml_result.xml')
    try:
        xml, files_size = get_analysis_xml(
                analysis_id=analysis_id,
                last_modified=last_modified,
                short=False)
    except AnalysisException as e:
        cart_logger.error('Error while composing metadata xml. %s' % str(e))
        content += render_to_string('xml/analysis_xml_summary.xml', {
                'counter': 0,
                'size': 0})
        return content
    formatted_xml = ''
    for s in xml_add_spaces(xml, space=4, tab=2):
            formatted_xml += s
    content += result_template.render(Context({
            'counter': 1,
            'xml': formatted_xml.strip()}))
    content += render_to_string('xml/analysis_xml_summary.xml', {
                    'counter': 1,
                    'size': str(round(files_size / 1073741824. * 100) / 100)})
    response = HttpResponse(content, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response
