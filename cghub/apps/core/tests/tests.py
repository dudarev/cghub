import codecs
import datetime
import os.path
import shutil
import sys
import time

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.simplejson import OrderedDict

from cghub_python_api import SOLRRequest
from mock import patch
from os import utime
from StringIO import StringIO
from urllib2 import URLError

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.template import Template, Context, RequestContext
from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.utils import timezone
from django.utils.importlib import import_module
from django.http import HttpRequest, QueryDict

from cghub.apps.cart.utils import Cart
from cghub import urls

from ..filters_storage import Filters, JSON_FILTERS_FILE_NAME
from ..forms import BatchSearchForm, AnalysisIDsForm
from ..management.commands.selectoptions import FiltersProcessor
from ..requests import (
        RequestFull, RequestDetail, RequestID, ResultFromSOLRFile,
        SearchByIDs, build_wsapi_xml, get_results_for_ids)
from ..templatetags.pagination_tags import Paginator
from ..templatetags.search_tags import (
        get_name_by_code, table_header, table_row, file_size,
        details_table, period_from_query, only_date, get_sample_type_by_code,
        data_menu)
from ..templatetags.core_tags import without_header, messages
from ..utils import (
        get_filters_dict, query_dict_to_str, paginator_params,
        generate_tmp_file_name, add_message, remove_message)
from ..views import error_500, error_404


def create_session(self):
    """
    Initialize session
    """
    settings.SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    store.save()
    self.session = store
    self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key


def get_request(url=reverse('home_page')):
    """
    Returns request object with session
    """
    # initialize session
    settings.SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    store.save()
    # create request
    factory = RequestFactory()
    request = factory.get(url)
    request.session = store
    request.cookies = {}
    request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
    return request


class CoreTestCase(TestCase):

    query = "6d54"

    def test_index(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('home_page'))
            self.assertEqual(response.status_code, 200)
            # check ajax urls is available
            self.assertContains(response, reverse('help_hint'))
            self.assertContains(response, reverse('help_text'))

    def test_index_redirect_to_search_if_get_specified(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get('/', {'state': '(live)'})
            self.assertRedirects(response, '%s?%s' % (
                    reverse('search_page'),
                    'state=%28live%29'))

    def test_open_help_page_in_new_tab(self):
        """
        Menu help link contains 'target="_blank"'.
        """
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('home_page'))
            self.assertContains(response, '<a href="%s?from=%s" target="_blank"' % (
                    reverse('help_page'), reverse('home_page')))
            # another behavior on help pages (Feature #2188)
            response = self.client.get(reverse('help_page'))
            self.assertNotContains(response, '<a href="%s?from=%s" target="_blank"' % (
                    reverse('help_page'), reverse('help_page')))
            self.assertContains(response, '<a href="%s"' % reverse('help_page'))

    def test_bad_filter(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('search_page'), {
                    'state': 'notexistent'})
            self.assertEqual(response.status_code, 200)

    def test_non_existent_search(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('search_page'), {
                    'q': 'non_existent_search_query'})
            self.assertEqual(response.status_code, 200)
            self.assertTrue('No results found' in response.content)

    def test_existent_search(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('search_page'), {
                    'q': '%s' % self.query})
            self.assertEqual(response.status_code, 200)
            # search by query alert (if no ids were found)
            self.assertContains(
                    response,
                    'The results maybe be incomplete or inconsistent due '
                    'to limited amount of textual metadata available.')

    def test_search_all(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            self.client.cookies[settings.REMEMBER_FILTERS_COOKIE] = 'true'
            response = self.client.get(reverse('search_page'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'No applied filters')
            # test empty last_query is saved
            response = self.client.get(reverse('home_page'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'No applied filters')

    def test_item_details_view(self):
        analysis_id = '916d1bd2-f503-4775-951c-20ff19dfe409'
        bad_analysis_id = 'badd1bd2-f503-4775-951c-123456789112'
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            try:
                response = self.client.get(reverse(
                        'item_details', kwargs={'analysis_id': bad_analysis_id}))
            except URLError as e:
                self.assertIn('No results for analysis_id', str(e))

            response = self.client.get(
                            reverse('item_details',
                            kwargs={'analysis_id': analysis_id}))
            self.assertEqual(response.status_code, 200)
            result = response.context['res']
            self.assertNotContains(response, u'No data.')
            self.assertContains(response, result['center_name'])
            # not ajax
            self.assertContains(response, '<head>')
            self.assertContains(response, '<script>LoadXMLString')
            self.assertContains(response, 'Add to cart')
            self.assertNotContains(response, 'In your cart')
            # TODO: add test for reason shows only for state != live
            # try ajax request
            response = self.client.get(
                            reverse('item_details',
                            kwargs={'analysis_id': analysis_id}),
                            {'ajax': 1},
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, result['center_name'])
            self.assertNotContains(response, '<script>LoadXMLString')
            self.assertContains(response, 'Show metadata XML')
            self.assertContains(response, 'Add to cart')
            self.assertNotContains(response, 'In your cart')
            # test if response contains some of needed fields
            self.assertContains(response, 'Modified')
            self.assertContains(response, 'Disease')
            self.assertContains(response, 'Disease Name')
            self.assertContains(response, 'Sample Accession')
            # test raw_xml
            self.assertTrue(response.context['raw_xml'])
            # check all entries are present
            self.assertIn('run_xml', response.context['raw_xml'])
            # check reason is present
            self.assertFalse(response.context['res']['reason'] is None)
            # test reason field
            analysis_id2 = '333a5cc4-741b-445c-93f9-9fde6f64b88f' # state = bad_data
            response = self.client.get(reverse(
                    'item_details', kwargs={'analysis_id': analysis_id2}))
            self.assertEqual(response.status_code, 200)
            # show 'Add to cart' button only if item not in cart
            create_session(self)
            cart = Cart(self.session)
            cart.add(result)
            response = self.client.get(
                            reverse('item_details',
                            kwargs={'analysis_id': analysis_id}))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, 'Add to cart')
            self.assertContains(response, 'In your cart')
            # try ajax request
            response = self.client.get(
                            reverse('item_details',
                            kwargs={'analysis_id': analysis_id}),
                            {'ajax': 1},
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, 'Add to cart')
            self.assertContains(response, 'In your cart')

    def test_save_filters_state(self):
        """
        Filters should be persistent only if 'remember filter settings' is checked.
        Only filters can be persistent, not query.
        """
        study = 'phs000178'
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(
                    '%s?state=(live)' % reverse('search_page'))
            self.assertEqual(
                    self.client.cookies.get(settings.LAST_QUERY_COOKIE).value,
                    'state=(live)')
            # save query
            response = self.client.get(
                    '%s?state=(live)&study=(%s)' % (reverse('search_page'), study))
            self.client.cookies[settings.REMEMBER_FILTERS_COOKIE] = 'true'
            response = self.client.get(reverse('home_page'))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, self.query)
            self.assertContains(response, 'data-filters="%s"' % study)
            # with referer from current site
            self.client.cookies[settings.REMEMBER_FILTERS_COOKIE] = 'false'
            response = self.client.get(
                    reverse('home_page'),
                    HTTP_REFERER=settings.SITE_DOMAIN)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'data-filters="%s"' % study)
            # `remember filters` is disabled and referer from outside
            response = self.client.get(reverse('home_page'))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, 'data-filters="%s"' % study)

    def test_save_limit_in_cookies(self):
        DEFAULT_FILTERS = {
                'study': ('phs000178', '*Other_Sequencing_Multiisolate'),
                'state': ('live',),
                'upload_date': '[NOW-7DAY+TO+NOW]'}
        with self.settings(DEFAULT_FILTERS=DEFAULT_FILTERS, PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(
                    '%s?%s' % (
                            reverse('search_page'),
                            query_dict_to_str(DEFAULT_FILTERS)))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                    response.cookies[settings.PAGINATOR_LIMIT_COOKIE].value,
                    str(settings.PAGINATOR_LIMITS[0]))
            response = self.client.get(
                    '%s?%s&limit=25' % (
                            reverse('search_page'),
                            query_dict_to_str(DEFAULT_FILTERS)))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.cookies[settings.PAGINATOR_LIMIT_COOKIE].value, '25')
            # test set limit in batch search
            data = {
                'text': '0005d2d0-aede-4f5c-89fa-aed12abfadd6 '
                '00007994-abeb-4b16-a6ad-7230300a29e9 '
                'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'}
            response = self.client.post(
                '%s?limit=10&offset=0' % reverse('batch_search_page'), data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.cookies[settings.PAGINATOR_LIMIT_COOKIE].value, '10')

    def test_custom_fields(self):
        """
        Test custom fields added in wsapi.Request.patch_result.
        See cghub.apps.core.utils.Request*.
        """
        analysis_id = '916d1bd2-f503-4775-951c-20ff19dfe409'
        api_request = RequestDetail(query={'analysis_id': analysis_id})
        result = api_request.call().next()
        self.assertEqual(api_request.hits, 1)
        self.assertTrue(result['files_size'] + 1)
        self.assertTrue(isinstance(result['checksum'], str))
        self.assertTrue(isinstance(result['filename'], str))

    def test_message_remove_view(self):
        create_session(self)
        response = self.client.get(reverse('message_remove', args=(1,)))
        self.assertEqual(response.status_code, 405)
        self.session['messages'] = {1: {
                'level': 'error', 'content': 'Some error!'}}
        self.session.save()
        response = self.client.post(
                reverse('message_remove', args=(2,)),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn(1, self.client.session['messages'])
        response = self.client.post(
                reverse('message_remove', args=(1,)),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(1, self.client.session['messages'])


class RequestsTestCase(TestCase):

    def test_search_by_ids(self):
        search = SearchByIDs(ids=['123'])
        self.assertTrue(search.is_empty())
        ids = [
            '916d1bd2-f503-4775-951c-20ff19dfe409',
            'TCGA-AZ-6608-11A-01D-1835-10'
        ]
        search = SearchByIDs(ids=ids)
        self.assertEqual(search.results, {
                'analysis_id': [{'analysis_id': '916d1bd2-f503-4775-951c-20ff19dfe409'}],
                'legacy_sample_id': [{'analysis_id': '860ca061-681b-46dc-8e15-db2a2cbe1c21'}]})
        self.assertFalse(search.is_empty())
        self.assertEqual(
                search.get_ids(),
                ['916d1bd2-f503-4775-951c-20ff19dfe409',
                '860ca061-681b-46dc-8e15-db2a2cbe1c21'])
        self.assertEqual(search.get_results(), [
                {'analysis_id': '916d1bd2-f503-4775-951c-20ff19dfe409'},
                {'analysis_id': '860ca061-681b-46dc-8e15-db2a2cbe1c21'}])
        # another Request class
        search = SearchByIDs(
                ids=['916d1bd2-f503-4775-951c-20ff19dfe409'],
                request_cls=RequestDetail)
        self.assertIn('platform', search.get_results()[0])


class UtilsTestCase(TestCase):
    IDS_IN_CART = ["4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6",
                   "4b2235d6-ffe9-4664-9170-d9d2013b395f"]
    FILES_IN_CART = {IDS_IN_CART[0]: {"state": "live"},
                     IDS_IN_CART[1]: {"state": "bad_data"}}

    def test_get_filters_dict(self):
        res = get_filters_dict({
                        'study': 'TGGA',
                        'center_name': 'BCM',
                        'bad_param': 'bad'})
        self.assertEqual(res, {'study': 'TGGA', 'center_name': 'BCM'})

    def test_query_dict_to_str(self):
        TEST_DATA_SET = [
            {
                'dict': {
                    'study': ['phs000178', '*Other_Sequencing_Multiisolate'],
                    'state': ('live',),
                    'upload_date': '[NOW-7DAY+TO NOW]'},
                'str': 'upload_date=[NOW-7DAY TO NOW]&study=(phs000178 OR *Other_Sequencing_Multiisolate)&state=(live)'
            }, {
                'dict': {
                'study': ('phs000178',),
                'state': 'live',
                'upload_date': '[NOW-7DAY TO NOW]'},
                'str': 'upload_date=[NOW-7DAY TO NOW]&study=(phs000178)&state=live'
            }, {
                'dict': {},
                'str': '',
            }
        ]

        for data in TEST_DATA_SET:
            self.assertEqual(query_dict_to_str(data['dict']), data['str'])

    def test_paginator_params(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            url = reverse('home_page')
            request = get_request(url=url)
            self.assertEqual(paginator_params(request), (0, 10))
            request.COOKIES[settings.PAGINATOR_LIMIT_COOKIE] = 25
            self.assertEqual(paginator_params(request), (0, 25))
            request = get_request(url=url + '?offset=10')
            self.assertEqual(paginator_params(request), (10, 10))
            request = get_request(url=url + '?limit=50')
            self.assertEqual(paginator_params(request), (0, 50))

    def test_generate_tmp_file_name(self):
        """
        smoke test for generate_tmp_file_name function
        """
        name = generate_tmp_file_name()
        self.assertIn('.tmp', name)

    def test_get_results_for_ids(self):
        ids = [
                '7850f073-642a-40a8-b49d-e328f27cfd66',
                '796e11c8-b873-4c37-88cd-18dcd7f287ec']
        results = get_results_for_ids(ids)
        # first is unchanged
        self.assertEqual(len(results), 2)
        # attributes was loaded for second item
        self.assertEqual(results[1]['disease_abbr'], 'COAD')

    def test_add_message(self):
        request = get_request()
        self.assertNotIn('messages', request.session)
        level = 'error'
        content = 'Some error!'
        message_id = add_message(
                request=request, level=level, content=content)
        self.assertIn('messages', request.session)
        self.assertIn(message_id, request.session['messages'])
        self.assertEqual(
                request.session['messages'][message_id],
                {'level': level, 'content': content, 'once': False})
        # test increase id
        self.assertNotIn(2, request.session['messages'])
        message_id = add_message(
                request=request, level=level, content=content)
        self.assertEqual(message_id, 2)
        self.assertIn(message_id, request.session['messages'])

        # test show once
        message_id = add_message(
                request=request, level=level,
                content=content, once=True)
        self.assertEqual(
                request.session['messages'][message_id],
                {'level': level, 'content': content, 'once': True})

        # test remove message
        remove_message(request=request, message_id=message_id)
        self.assertNotIn(message_id, request.session['messages'])


class ContextProcessorsTestCase(TestCase):

    def test_settings(self):
        # test cghub.apps.core.context_processors.settings
        MANY_FILES = 101
        SUPPORT_EMAIL = 'some@email.com'
        TOOLTIP_HOVER_TIME = 250
        with self.settings(
                MANY_FILES=MANY_FILES,
                SUPPORT_EMAIL=SUPPORT_EMAIL,
                TOOLTIP_HOVER_TIME=TOOLTIP_HOVER_TIME):
            factory = RequestFactory()
            request = factory.get('/')
            context = RequestContext(request)
            self.assertEqual(context['MANY_FILES'], MANY_FILES)
            self.assertEqual(context['SUPPORT_EMAIL'], SUPPORT_EMAIL)
            self.assertEqual(context['TOOLTIP_HOVER_TIME'], TOOLTIP_HOVER_TIME)


class TemplateTagsTestCase(TestCase):

    def test_sort_link_tag(self):
        test_request = HttpRequest()
        test_request.path = reverse('search_page')
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(
            out,
            '<a class="sort-link" href="/search/?sort_by=last_modified" '
            'title="click to sort by Date Uploaded">Date Uploaded</a>')

        test_request.path = ''
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(
            out,
            '<a class="sort-link" href="/search/?sort_by=last_modified" '
            'title="click to sort by Date Uploaded">Date Uploaded</a>')

        # make sure that other request.GET variables are preserved
        test_request.GET.update({'q': 'sample_query'})
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(
            out,
            '<a class="sort-link" href="/search/?q=sample_query&amp;sort_by=last_modified" '
            'title="click to sort by Date Uploaded">Date Uploaded</a>')

        # make sure that direction label is rendered if it is active sort filter
        del(test_request.GET['q'])
        test_request.GET.update({'sort_by': 'last_modified'})
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(
            out,
            '<a class="sort-link" href="/search/?sort_by=-last_modified" '
            'title="click to sort by Date Uploaded">Date Uploaded'
            '<span class="down-triangle"></span></a>')
        # test sorting on cart page
        test_request.path = reverse('cart_page')
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'study' 'Study' %}"
        ).render(Context({
            'request': test_request
        }))
        self.assertIn('sort_by=study', out)

    def test_applied_filters_tag(self):
        request = HttpRequest()
        request.GET.update({
            'study': '(phs000178)',
            'center_name': '(HMS-RK)',
            'library_strategy': '(WGS OR WXS)',
            'last_modified': '[NOW-7DAY TO NOW]',
            'disease_abbr': '(CNTL OR COAD)',
            'refassem_short_name': '(HG18)',
            'q': 'Some text'})
        template = Template("{% load search_tags %}{% applied_filters request %}")
        result = template.render(RequestContext(request, {}))
        self.assertEqual(
            result,
            u'Applied filter(s): <ul><li data-name="q" data-filters="Some text">'
            '<b>Text query</b>: "Some text"</li><li data-name="center_name" data-filters="HMS-RK">'
            '<b>Center</b>: <span>HMS-RK</span></li><li data-name="refassem_short_name" data-filters="HG18">'
            '<b>Assembly</b>: <span>HG18</span></li><li data-name="last_modified" data-filters="[NOW-7DAY TO NOW]">'
            '<b>Modified</b>: last week</li><li data-name="disease_abbr" data-filters="CNTL&amp;COAD">'
            '<b>Disease</b>: <span>Controls (CNTL)</span>, <span>Colon adenocarcinoma (COAD)</span>'
            '</li><li data-name="study" data-filters="phs000178"><b>Study</b>: <span>TCGA (phs000178)</span>'
            '</li><li data-name="library_strategy" data-filters="WGS&amp;WXS">'
            '<b>Library Type</b>: <span>WGS</span>, <span>WXS</span></li></ul>')

    def test_items_per_page_tag(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            request = HttpRequest()
            default_limit = settings.PAGINATOR_LIMITS[0]
            default_limit_link = ('<a href="?limit={limit}&amp;offset=0"><span class="hidden">'
                    'view </span>{limit}'.format(limit=default_limit))

            request.GET = QueryDict('', mutable=False)
            template = Template(
                    "{% load pagination_tags %}{% items_per_page request %}")
            result = template.render(RequestContext(request, {}))
            self.assertIn('<a href="?limit=50&amp;offset=0"><span class="hidden">view </span>50', result)
            self.assertNotIn(default_limit_link, result)

            request.GET = QueryDict('limit=50', mutable=False)
            result = template.render(RequestContext(request, {}))
            self.assertNotIn(
                    '<a href="?limit=50" title="View 50 items per page">50</a>',
                    result)
            self.assertIn(default_limit_link, result)

            # test offset
            # offset=10, limit=10 -> offset=0, limit=25
            # offset=20, limit=10 -> offset=0, limit=25
            # offset=30, limit=10 -> offset=25, limit=25
            template = Template(
                    "{% load pagination_tags %}{% items_per_page request %}")
            request.GET = QueryDict('limit=10&offset=10', mutable=False)
            result = template.render(RequestContext(request, {}))
            self.assertNotIn('offset=10', result)
            self.assertIn('offset=0', result)
            request.GET = QueryDict('limit=10&offset=30', mutable=False)
            result = template.render(RequestContext(request, {}))
            self.assertNotIn('offset=10', result)
            self.assertIn('offset=25', result)

    def test_get_name_by_code_tag(self):
        for section, section_data in Filters.get_all_filters().iteritems():
            if section == "sample_type":
                try:
                    for code, name in section_data[key].iteritems():
                        get_name_by_code(section, code)
                        assert False
                except Exception as e:
                    assert e.message == 'Use get_sample_type_by_code tag for sample types.'
            else:
                key = 'filters'
                for code, name in section_data[key].iteritems():
                    assert (get_name_by_code(section, code) == name)

        assert (get_name_by_code('unknown_section', 'unknown_code') ==
                'unknown_code')

    def test_file_size_filter(self):
        self.assertEqual(file_size('123'), '123 Bytes')
        self.assertEqual(file_size(123456).replace('.', ','), '120,56 KB')
        self.assertEqual(file_size(1234567).replace('.', ','), '1,18 MB')
        self.assertEqual(file_size(1234567890).replace('.', ','), '1,15 GB')

    def test_table_header_tag(self):
        COLUMNS = ('Disease', 'Analysis Id', 'Study')
        request = HttpRequest()
        with self.settings(TABLE_COLUMNS = COLUMNS[:2]):
            res = table_header(request)
            self.assertTrue('<th' in res)
            self.assertTrue(COLUMNS[0] in res)
            self.assertTrue(COLUMNS[1] in res)
            self.assertTrue('visible' in res)
            self.assertTrue('hidden' not in res)
            self.assertTrue(COLUMNS[2] not in res)

    def test_table_row_tag(self):
        COLUMNS = ('Disease', 'Analysis Id', 'Study')
        RESULT = {
                'disease_abbr': 'COAD',
                'analysis_id': '6cca55c6-3748-4c05-8a31-0b1a125b39f5',
                'study': 'phs000178',
                }
        with self.settings(TABLE_COLUMNS = COLUMNS[:2]):
            res = table_row(RESULT)
            self.assertTrue('<td' in res)
            self.assertTrue(RESULT['disease_abbr'] in res)
            self.assertTrue(RESULT['analysis_id'] in res)
            self.assertTrue(RESULT['study'] not in res)
        # test value_resolvers
        right_value = 'Right value'

        def value_resolver(value, result):
            self.assertIn('analysis_id', result)
            return right_value

        with self.settings(VALUE_RESOLVERS={'Study': value_resolver}):
            res = table_row(RESULT)
            self.assertIn(right_value, res)
            self.assertNotIn(RESULT['study'], res)

    def test_details_table_tag(self):
        FIELDS = ('Analysis Id', 'Study')
        RESULT = {
                'analysis_id': '6cca55c6-3748-4c05-8a31-0b1a125b39f5',
                'study': 'phs000178',
                }
        with self.settings(DETAILS_FIELDS = FIELDS):
            res = details_table(RESULT)
            self.assertTrue(res.find('<td') != -1)
            for field in FIELDS:
                self.assertTrue(res.find(field) != -1)
        # test value_resolvers
        right_value = 'Right value'

        def value_resolver(value, values):
            return right_value

        with self.settings(VALUE_RESOLVERS={'Study': value_resolver}):
            res = table_row(RESULT)
            self.assertIn(right_value, res)
            self.assertNotIn(RESULT['study'], res)

    def test_data_menu(self):

        def example_menu1(values):
            return values.get('study') + '+'

        def example_menu2(values):
            return values.get('study') + '-'

        with self.settings(ROW_MENU_ITEMS=[
                ('Example menu 1', example_menu1),
                ('Example menu 2', example_menu2)]):
            self.assertEqual(data_menu({'study': 'TCGA'}),
            'Example menu 1|TCGA+,Example menu 2|TCGA-')

    def test_period_from_query(self):
        test_data = (
            {
                'query': '[NOW-2DAY TO NOW]',
                'result': '2013/02/25 - 2013/02/27'},
            {  # test with quoted
                'query': '[NOW-2DAY%20TO%20NOW]',
                'result': '2013/02/25 - 2013/02/27'},
            {
                'query': '[NOW-20DAY TO NOW]',
                'result': '2013/02/07 - 2013/02/27'},
            {
                'query': '[NOW-5DAY TO NOW-2]',
                'result': '2013/02/22 - 2013/02/25'},
            {
                'query': '[BAD TO NOW-2]',
                'result': ''},
            {
                'query': '',
                'result': ''},
        )
        with patch.object(timezone, 'now', return_value=datetime.datetime(2013, 2, 27)) as mock_now:
            for data in test_data:
                self.assertEqual(
                        period_from_query(data['query']),
                        data['result'])

    def test_only_date_tag(self):
        self.assertEqual(only_date('2013-02-22T12:00:21Z'), '2013-02-22')
        self.assertEqual(only_date('2013-02-22'), '2013-02-22')
        self.assertEqual(only_date(''), '')

    def test_double_digit_for_sample_type(self):
        """
        Sample type:
        "07", "Additional Metastatic", "TAM"
        """
        self.assertEqual(get_sample_type_by_code('07', 'shortcut'), 'TAM')
        self.assertEqual(get_sample_type_by_code(7, 'shortcut'), 'TAM')

    def test_without_header(self):
        """
        Removes header like this:
        <?xml version="1.0" encoding="ASCII" standalone="yes"?>
        """
        xml = u'<?xml version="1.0" encoding="ASCII" standalone="yes"?><analysis>123</analysis>'
        self.assertEqual(without_header(xml), u'<analysis>123</analysis>')
        xml = u' <?xml version="1.0" encoding="ASCII" standalone="yes"?><analysis>123</analysis>'
        self.assertEqual(
                without_header(xml),
                u' <?xml version="1.0" encoding="ASCII" standalone="yes"?><analysis>123</analysis>')
        xml = u'<analysis>123</analysis>'
        self.assertEqual(without_header(xml), u'<analysis>123</analysis>')
        self.assertEqual(without_header(None), u'')

    def test_messages(self):
        request = get_request()
        self.assertNotIn('messages', request.session)
        result = messages({'request': request})
        self.assertEqual(result, '')
        request.session['messages'] = {}
        result = messages({'request': request})
        self.assertEqual(result, '')
        level = 'error'
        content = 'Some error!'
        request.session['messages'][1] = {
                'level': level, 'content': content,
                'once': False}
        result = messages({'request': request})
        self.assertIn('alert-%s' % level, result)
        self.assertIn('1', result)
        self.assertIn(content, result)
        # test show message once
        result = messages({'request': request})
        self.assertIn('alert-%s' % level, result)
        request.session['messages'][1]['once'] = True
        result = messages({'request': request})
        self.assertIn('alert-%s' % level, result)
        result = messages({'request': request})
        self.assertNotIn('alert-%s' % level, result)
        # test show messages from context
        result = messages({'notifications': [
                {'level': level, 'content': content}
            ]})
        self.assertIn('alert-%s' % level, result)
        self.assertNotIn('1', result)
        self.assertIn(content, result)


class SelectFiltersTestCase(TestCase):

    def test_filters_storrage_update(self):
        """
        Test Filters class
        """
        if not os.path.exists(JSON_FILTERS_FILE_NAME):
            shutil.copyfile(
                    '%s.default' % JSON_FILTERS_FILE_NAME,
                    JSON_FILTERS_FILE_NAME)
            time.sleep(1)
        old_argv = sys.argv
        sys.argv = []
        new_filters = {'somefilter': 'Filter name'}
        self.assertNotEqual(
                Filters.get_all_filters()['study']['filters'],
                new_filters)
        Filters._ALL_FILTERS['study']['filters'] = new_filters
        self.assertEqual(
                Filters.get_all_filters()['study']['filters'],
                new_filters)
        # touch file
        with file(JSON_FILTERS_FILE_NAME, 'a'):
            utime(JSON_FILTERS_FILE_NAME, None)
        self.assertNotEqual(
                Filters.get_all_filters()['study']['filters'],
                new_filters)
        with file(JSON_FILTERS_FILE_NAME, 'a'):
            utime(JSON_FILTERS_FILE_NAME, None)
        sys.argv = old_argv

    def test_selectoptions(self):
        """
        filters_storage.json.test will be used while testing
        """
        # test FiltersProcessor
        options = OrderedDict([
            ('NCBI37/HG19', OrderedDict([
                ('HG19', 'HG19'),
                ('HG19_Broad_variant', 'HG19_Broad_variant'),
                ('NCBI37', OrderedDict([
                    ('NCBI37_BCCAGSC_variant', 'NCBI37_BCCAGSC_variant'),
                    ('NCBI37_BCM_variant', 'NCBI37_BCM_variant'),
                ])),
            ])),
            ('Empty', OrderedDict([])),
            ('GRCh37', 'GRCh37'),
        ])
        filter_name = 'refassem_short_name'
        stdout = StringIO()
        stderr = StringIO()
        processor = FiltersProcessor(
                stdout=stdout, stderr=stderr, verbosity=1)
        options = processor.process(
                filter_name=filter_name, options=options,
                select_options=False)
        self.assertEqual(
            options,
            OrderedDict([
                ('HG19 OR HG19_Broad_variant OR NCBI37_BCCAGSC_variant OR NCBI37_BCM_variant', 'NCBI37/HG19'),
                ('HG19', '-HG19'),
                ('HG19_Broad_variant', '-HG19_Broad_variant'),
                ('NCBI37_BCCAGSC_variant OR NCBI37_BCM_variant', '-NCBI37'),
                ('NCBI37_BCCAGSC_variant', '--NCBI37_BCCAGSC_variant'),
                ('NCBI37_BCM_variant', '--NCBI37_BCM_variant'),
                ('GRCh37', 'GRCh37')]
            )
        )
        # test FiltersProcessor.check_in_all_options
        processor.all_options = ['abcd', 'xyz', 'cbcd']
        self.assertEqual(processor.check_in_all_options('*bcd'), ['abcd', 'cbcd'])
        self.assertEqual(processor.check_in_all_options('x*'), ['xyz'])
        self.assertEqual(processor.check_in_all_options('abcd'), ['abcd'])
        self.assertEqual(processor.check_in_all_options('nnn'), [])


    def test_pagination_templatetag(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            request = HttpRequest()
            request.GET = {'offset': '20', 'limit': '10'}
            request.path = reverse('search_page')
            result = Template(
                "{% load pagination_tags %}"
                "{% pagination %}"
            ).render(Context({
                'request': request,
                'num_results': 103,

            }))
            self.assertIn(
                '<a href="/search/?offset=10&amp;limit=10">Prev<span class="hidden"> page</span></a>',
                result)
            self.assertIn(
                '<li><a href="/search/?offset=0&amp;limit=10"><span class="hidden">page </span>1</a></li>',
                result)
            self.assertIn(
                '<li class="disabled"><a href="javascript:void(0)"><span class="hidden">page </span>...</a></li>',
                result)


class BatchSearchTestCase(TestCase):

    def test_batch_search_form(self):
        ids = [
            '0005d2d0-aede-4f5c-89fa-aed12abfadd6',
            '00007994-abeb-4b16-a6ad-7230300a29e9',
            '000f332c-7fd9-4515-bf5f-9b77db43a3fd',
            '00007994-abeb-4b16-a6ad-7230300a29e9',
            'TCGA-04-1337-01A-01W-0484-10',
            # different cases
            'TcGA-04-1337-01e-01w-0455-12',
            '11107994-AbEb-4D16-a6ad-7230300a29A9',
        ]
        f = SimpleUploadedFile(name='ids.csv', content=' '.join(ids))
        form = BatchSearchForm({'text': ' '.join(ids)})
        self.assertTrue(form.is_valid())
        form = BatchSearchForm({}, {'upload': f})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data['ids']), 6)
        for id in ids:
            self.assertTrue(
                    (id.lower() in form.cleaned_data['ids']) or
                    (id.upper() in form.cleaned_data['ids']))
        self.assertEqual(len(form.cleaned_data['unvalidated_ids']), 0)
        form = BatchSearchForm({})
        self.assertFalse(form.is_valid())
        # test unsuported format
        form = BatchSearchForm({
                'text': 'somebadids 00007994-abeb-4b16-a6ad-7230300a29e9'})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data['unvalidated_ids']), 1)
        # unsupported file format
        f = SimpleUploadedFile(name='ids.csv', content='badcontent ')
        form = BatchSearchForm({}, {'upload': f})
        self.assertFalse(form.is_valid())

    def test_batch_search_view(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('batch_search_page'))
            self.assertEqual(response.status_code, 200)
            # submit wrong data
            data = {'text': 'badtext'}
            response = self.client.post(reverse('batch_search_page'), data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'No valid ids were found')
            # submit not existed analysis_id
            data = {
                'text': '0005d2d0-aede-4f5c-89fa-aed12abfadd6 '
                '00007994-abeb-4b16-a6ad-7230300a29e9 '
                'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'}
            response = self.client.post(reverse('batch_search_page'), data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Found by analysis_id: 2')
            # some items were deleted
            ids = response.content
            ids = ids[ids.find('<textarea'):ids.find('</textarea>')]
            ids = ids[ids.find('>') + 1:]
            create_session(self)
            data = {'ids': ids}
            response = self.client.post(reverse('batch_search_page'), data)
            self.assertEqual(response.status_code, 200)
            # ok, adding files to cart
            data = {'ids': ids, 'add_to_cart': 'true'}
            response = self.client.post(reverse('batch_search_page'), data)
            self.assertRedirects(response, reverse('cart_page'))
            cart = Cart(session=self.client.session)
            self.assertEqual(cart.all_count, 2)
            # redirect to batch_search_page if all items were deleted
            data = {'ids': ''}
            response = self.client.post(reverse('batch_search_page'), data)
            self.assertRedirects(response, reverse('batch_search_page'))

    def test_analysis_ids_form(self):
        data = {
            'ids': '0005d2d0-aede-4f5c-89fa-aed12abfadd6 '
            '00007994-abeb-4b16-a6ad-7230300a29e9 '
            'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'}
        form = AnalysisIDsForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data['ids']), 3)


class SearchViewPaginationTestCase(TestCase):

    query = "6d54"

    def setUp(self):
        api_request = RequestID(query={'all_metadata': self.query})
        self.results = []
        for result in api_request.call():
            self.results.append(result)
        self.default_results_count = api_request.hits

    def test_pagination_default_pagination(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('search_page') +
                                       '?q={query}&offset={offset}&limit={limit}'.format(
                                           query=self.query, offset=None, limit=None))
            self.assertContains(response, '1')
            self.assertContains(response, '2')
            self.assertContains(response, 'Prev')
            self.assertContains(response, 'Next')

    def test_pagination_one_page_limit_pagination(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(
                reverse('search_page') +
                '?q={query}&offset={offset}&limit={limit}'.format(
                    query=self.query, offset=0, limit=self.default_results_count))
            self.assertContains(response, '1')
            self.assertContains(response, 'active')
            # Prev and Next are both disabled
            self.assertContains(response, 'disabled', 2)
            self.assertContains(response, 'Prev')
            self.assertContains(response, 'Next')

    def test_pagination_one_per_page_limit_pagination(self):
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(reverse('search_page') +
                                       '?q={query}&offset={offset}&limit={limit}'.format(
                                           query=self.query, offset=0, limit=1))
            self.assertContains(response, 'active')
            self.assertContains(response, 'Prev')
            self.assertContains(response, 'Next')

    def test_pagination_limit_saved_in_cookie(self):
        """
        If offset is not specified in get, then will be used
        offset saved in cookie or default offset.
        """
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            request = get_request()
            context = {'request': request, 'num_results': 100}
            result = Paginator(context)
            self.assertEqual(result.pages_count, 10)
            context['request'].COOKIES[settings.PAGINATOR_LIMIT_COOKIE] = 25
            result = Paginator(context)
            self.assertEqual(result.pages_count, 4)

    def test_redirect_from_home_page(self):
        """
        Test redirect from home page if any GET parameters are specified.
        """
        with self.settings(PAGINATOR_LIMITS=[10, 25, 50]):
            response = self.client.get(
                reverse('home_page') + '?q={query}'.format(query=self.query),
                follow=True)
            self.assertTrue('search' in response.redirect_chain[0][0])


class MetadataViewTestCase(TestCase):

    """
    Cached files will be used
    7b9cd36a-8cbb-4e25-9c08-d62099c15ba1 - 2012-10-29T21:56:12Z
    """
    analysis_id = '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1'
    last_modified = '2013-05-16T20:50:58Z'

    def test_metadata(self):
        path = os.path.join(
                settings.FULL_METADATA_CACHE_DIR, self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        response = self.client.get(
                    reverse('metadata',
                    args=[self.analysis_id]),
                    {'last_modified': self.last_modified})
        content = response.content
        self.assertTrue(self.analysis_id in content)
        self.assertEqual(response['Content-Type'], 'text/xml')
        self.assertIn(
                'attachment; filename=metadata.xml',
                response['Content-Disposition'])
        if os.path.isdir(path):
            shutil.rmtree(path)


class SettingsTestCase(TestCase):

    def test_table_columns_and_details_fields(self):
        """
        Check that all names from
        settings.TABLE_COLUMNS and
        settings.DETAILS_FILEDS exists
        """
        from cghub.apps.core.attributes import COLUMN_NAMES
        from cghub.apps.core.templatetags.search_tags import field_values

        analysis_id = '916d1bd2-f503-4775-951c-20ff19dfe409'
        names = list(settings.TABLE_COLUMNS)
        for name in names:
            self.assertIn(name, COLUMN_NAMES)
        for name in settings.DETAILS_FIELDS:
            if name not in names:
                names.append(name)
        api_request = RequestDetail(query={'analysis_id': analysis_id})
        result = api_request.call().next()
        self.assertEqual(api_request.hits, 1)
        field_values_dict = field_values(result)
        for name in names:
            if name == 'Files':
                self.assertTrue(len(result['files']))
                continue
            self.assertIn(name, field_values_dict)


class ErrorViewsTestCase(TestCase):

    def test_error_404(self):
        self.assertTrue(urls.handler404.endswith('.error_404'))
        factory = RequestFactory()
        request = factory.get('/')
        response = error_404(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn('This page was not found.', response.content)

    def test_error_500(self):
        self.assertTrue(urls.handler500.endswith('.error_500'))
        factory = RequestFactory()
        request = factory.get('/')
        r = error_500(request)
        self.assertEqual(r.status_code, 500)
        self.assertIn('Internal server error.', r.content)
        error_value = 'some val'
        with patch.object(sys, 'exc_info', return_value=(URLError, error_value, 'some_tb')) as mock_exc_info:
            r = error_500(request)
            self.assertEqual(r.status_code, 500)
            self.assertTrue(str(r).find(error_value) != -1)
        # Details should be shown only for URLError exception
        with patch.object(sys, 'exc_info', return_value=(AttributeError, error_value, 'some_tb')) as mock_exc_info:
            r = error_500(request)
            self.assertEqual(r.status_code, 500)
            self.assertTrue(str(r).find(error_value) == -1)
