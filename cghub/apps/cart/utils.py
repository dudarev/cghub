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

from cghub.apps.core.attributes import CART_SORT_ATTRIBUTES
from cghub.apps.core.templatetags.search_tags import field_values
from cghub.apps.core.requests import RequestDetailJSON, get_results_for_ids
from cghub.apps.core.utils import CSVUnicodeWriter, add_message, Gzipper

from .cache import AnalysisException, get_analysis_xml
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

    def page(self, offset=0, limit=10, sort_by=None):
        if (sort_by and sort_by not in CART_SORT_ATTRIBUTES and
                        sort_by[1:] not in CART_SORT_ATTRIBUTES):
            sort_by = None
        if sort_by:
            if sort_by[0] == '-':
                sort_str = '-analysis__%s' % sort_by[1:]
            else:
                sort_str = 'analysis__%s' % sort_by
            items = self.cart.items.order_by(sort_str)[offset:offset + limit]
        else:    
            items = self.cart.items.all()[offset:offset + limit]
        if not items.exists():
            return []
        results = get_results_for_ids([i.analysis.analysis_id for i in items])
        if sort_by:
            sort_attribute = sort_by[1:] if sort_by[0] == '-' else sort_by
            sort_key = lambda s: s[sort_attribute]
            results.sort(key=sort_key, reverse=sort_by[0].find('-') == 0)
        return results

    def add(self, result):
        analysis_id = result['analysis_id']
        try:
            analysis = Analysis.objects.get(analysis_id=analysis_id)
            if analysis.last_modified != result['last_modified']:
                # update analysis
                analysis.state = result['state']
                analysis.files_size = result['files_size']
                analysis.last_modified = result['last_modified']
                analysis.save()
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
        self.session['cart_count'] = self.cart.items.count()
        self.session.modified = True


def manifest_xml_generator(request, compress=False):
    """
    Return manifest xml for cart items with state==live.

    :param request: django Request object
    :param compress: set to True to enable compression 
    """
    cart = Cart(request.session)
    zipper = Gzipper(filename='manifest.xml', compress=compress)
    count_live = cart.live_count
    zipper.write(render_to_string('xml/analysis_xml_header.xml', {
                        'date': datetime.datetime.strftime(
                                    timezone.now(), '%Y-%d-%m %H:%M:%S'),
                        'len': count_live}))
    iterator = cart.cart.items.filter(analysis__state='live').iterator()
    counter = 0
    downloadable_size = 0
    result_template = get_template('xml/manifest_xml_result.xml')
    while True:
        ids = []
        for i in xrange(settings.MAX_ITEMS_IN_QUERY):
            try:
                ids.append(next(iterator).analysis.analysis_id)
            except StopIteration:
                break
        if not ids:
            break
        api_request = RequestDetailJSON(query={'analysis_id': ids})
        for result in api_request.call():
            downloadable_size += result['files_size']
            counter += 1
            zipper.write(result_template.render(Context({
                    'counter': counter,
                    'result': result})))
        yield zipper.read()
    if counter != count_live:
        cart_logger.error('Error while composing manifest xml.')
        add_message(
                request=request,
                level='error',
                content='An error occured while composing manifest xml.')
        request.session.save()
    else:
        zipper.write(render_to_string('xml/analysis_xml_summary.xml', {
                    'counter': counter,
                    'size': str(round(downloadable_size / 1073741824. * 100) / 100)}))
    yield zipper.close()


def metadata_xml_generator(request, compress=False):
    """
    Return metadata xml for all cart items.

    :param request: django Request object
    :param compress: set to True to enable compression 
    """
    cart = Cart(request.session)
    zipper = Gzipper(filename='metadata.xml', compress=compress)
    items = cart.cart.items.all()
    zipper.write(render_to_string('xml/analysis_xml_header.xml', {
                        'date': datetime.datetime.strftime(
                                    timezone.now(), '%Y-%d-%m %H:%M:%S'),
                        'len': items.count()}))
    counter = 0
    downloadable_size = 0
    result_template = get_template('xml/metadata_xml_result.xml')
    for item in items:
        analysis = item.analysis
        try:
            xml, files_size = get_analysis_xml(
                            analysis_id=analysis.analysis_id,
                            last_modified=analysis.last_modified)
        except AnalysisException as e:
            cart_logger.error('Error while composing metadata xml. %s' % str(e))
            add_message(
                    request=request,
                    level='error',
                    content='An error occured while composing metadata/manifest xml file.')
            request.session.save()
            return
        counter += 1
        downloadable_size += analysis.files_size
        zipper.write(result_template.render(Context({
                    'counter': counter,
                    'xml': xml.strip()})))
        yield zipper.read()
    zipper.write(render_to_string('xml/analysis_xml_summary.xml', {
                    'counter': counter,
                    'size': str(round(downloadable_size / 1073741824. * 100) / 100)}))
    yield zipper.close()


def summary_tsv_generator(request, compress=False):
    """
    Return summary tsv for all cart items.

    :param request: django Request object
    :param compress: set to True to enable compression 
    """
    cart = Cart(request.session)
    zipper = Gzipper(filename='summary.tsv', compress=compress)
    COLUMNS = settings.TABLE_COLUMNS
    stringio = StringIO()
    csvwriter = CSVUnicodeWriter(
            stringio, quoting=csv.QUOTE_MINIMAL,
            dialect='excel-tab', lineterminator='\n')
    csvwriter.writerow(
            [field.lower().replace(' ', '_') for field in COLUMNS])
    count_all = cart.all_count
    iterator = cart.cart.items.all().iterator()
    count = 0
    while True:
        ids = []
        for i in xrange(settings.MAX_ITEMS_IN_QUERY):
            try:
                ids.append(next(iterator).analysis.analysis_id)
            except StopIteration:
                break
        if not ids:
            break
        api_request = RequestDetailJSON(query={'analysis_id': ids})
        for result in api_request.call():
            fields = field_values(result, humanize_files_size=False)
            row = []
            for field_name in COLUMNS:
                value = fields.get(field_name, '')
                row.append(unicode(value))
            csvwriter.writerow(row)
            count += 1
        stringio.seek(0)
        line = stringio.read()
        stringio.seek(0)
        stringio.truncate()
        zipper.write(line)
        yield zipper.read()
    if count != count_all:
        cart_logger.error('Error while composing summary tsv.')
        add_message(
                request=request,
                level='error',
                content='An error occured while composing summary tsv.')
        request.session.save()
        zipper.write(u'\nError!')
    yield zipper.close()


def item_metadata(analysis_id, last_modified):
    content = render_to_string('xml/analysis_xml_header.xml', {
                        'date': datetime.datetime.strftime(
                                    timezone.now(), '%Y-%d-%m %H:%M:%S'),
                        'len': 1})
    result_template = get_template('xml/metadata_xml_result.xml')
    try:
        xml, files_size = get_analysis_xml(
                analysis_id=analysis_id,
                last_modified=last_modified)
    except AnalysisException as e:
        cart_logger.error(
                'Error while composing metadata xml. %s' % str(e))
        content += render_to_string('xml/analysis_xml_summary.xml', {
                'counter': 0,
                'size': 0})
        return content
    content += result_template.render(Context({
            'counter': 1,
            'xml': xml.strip()}))
    content += render_to_string('xml/analysis_xml_summary.xml', {
                    'counter': 1,
                    'size': str(round(files_size / 1073741824. * 100) / 100)})
    response = HttpResponse(content, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response
