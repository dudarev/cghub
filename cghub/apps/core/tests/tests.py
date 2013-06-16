import os
import sys
import shutil
import contextlib
import datetime
import urllib2

from urllib2 import URLError
from lxml import objectify
from mock import patch
from djcelery.models import TaskState
from celery import states

from django.conf import settings
from django.utils import simplejson as json
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.test.client import RequestFactory
from django.template import Template, Context, RequestContext
from django.http import HttpRequest, QueryDict
from django.utils.importlib import import_module
from django.contrib.sessions.models import Session

from cghub.wsapi.api import Results
from cghub.wsapi.utils import makedirs_group_write

from cghub.apps.core.templatetags.pagination_tags import Paginator
from cghub.apps.core.templatetags.search_tags import (get_name_by_code,
                    table_header, table_row, file_size, details_table,
                    period_from_query, only_date, get_sample_type_by_code)
from cghub.apps.core.utils import (WSAPI_SETTINGS_LIST, get_filters_string,
                    get_wsapi_settings, get_default_query,
                    generate_task_id, is_task_done,
                    decrease_start_date, xml_add_spaces, paginator_params)
from cghub.apps.core.views import error_500
from cghub.apps.core.filters_storage import ALL_FILTERS

from cghub.apps.cart.views import cart_add_files


TEST_DATA_DIR = 'cghub/test_data/'


def get_request(url=reverse('home_page')):
    """
    Returns request object with session
    """
    # initialize session
    settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    store.save()
    # create request
    factory = RequestFactory()
    request = factory.get(url)
    request.session = store
    request.cookies = {}
    request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
    # create session
    s = Session(
            expire_date=timezone.now() + datetime.timedelta(days=7),
            session_key=store.session_key)
    s.save()
    return request


class WithCacheTestCase(TestCase):

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        # cache filenames are generated as following:
        # >>> from wsapi.cache import get_cache_file_name
        # >>> get_cache_file_name('xml_text=6d5%2A', True)
        # u'/tmp/wsapi/427dcd2c78d4be27efe3d0cde008b1f9.xml'

        # wsapi cache
        if not os.path.exists(settings.WSAPI_CACHE_DIR):
            makedirs_group_write(settings.WSAPI_CACHE_DIR)
        for f in self.wsapi_cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(settings.WSAPI_CACHE_DIR, f)
            )
        if self.wsapi_cache_files:
            path = os.path.join(settings.WSAPI_CACHE_DIR, self.wsapi_cache_files[0])
            if not os.path.exists(path):
                return
            self.default_results = objectify.fromstring(
                open(path).read())
            self.default_results_count = len(self.default_results.findall('Result'))

    def tearDown(self):
        # wsapi cache
        for f in self.wsapi_cache_files:
            path = os.path.join(settings.WSAPI_CACHE_DIR, f)
            if not os.path.exists(path):
                continue
            os.remove(path)
        # cart cache
        for f in self.cart_cache_files:
            path = os.path.join(
                    settings.CART_CACHE_DIR, f[:2], f[2:4], f)
            if os.path.isdir(path):
                # remove cart cache
                shutil.rmtree(path)


class CoreTestCase(WithCacheTestCase):

    cart_cache_files = []
    wsapi_cache_files = [
        '24f05bdcef000bb97ce1faac7ed040ee.xml',
        '4cc5fcb1fd66e39cddf4c90b78e97667.xml',
        '7cd2c2b431595c744b22c0c21daa8763.ids',
        '80854b20d08c55ed41234dc62fff82c8.ids',
        '6cc087ba392e318a84f3d1d261863728.ids',
    ]
    query = "6d54"

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # check ajax urls is available
        self.assertContains(response, reverse('help_hint'))
        self.assertContains(response, reverse('help_text'))
        self.assertContains(response, reverse('celery_task_status'))

    def test_non_existent_search(self):
        response = self.client.get('/search/?q=non_existent_search_query')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No results found' in response.content)

    def test_existent_search(self):
        response = self.client.get('/search/?q=%s' % self.query)
        self.assertEqual(response.status_code, 200)

    def test_item_details_view(self):
        analysis_id = '12345678-1234-1234-1234-123456789abc'
        response = self.client.get(reverse('item_details', kwargs={'analysis_id': analysis_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'No data.')

        from cghub.wsapi.api import request as api_request
        file_name = os.path.join(settings.WSAPI_CACHE_DIR, self.wsapi_cache_files[0])
        results = api_request(file_name=file_name)
        self.assertTrue(hasattr(results, 'Result'))
        response = self.client.get(
                        reverse('item_details',
                        kwargs={'analysis_id': results.Result.analysis_id}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, u'No data.')
        self.assertContains(response, results.Result.center_name)
        # not ajax
        self.assertContains(response, '<head>')
        self.assertContains(response, 'Collapse all')
        self.assertContains(response, 'Expand all')
        # try ajax request
        response = self.client.get(
                        reverse('item_details',
                        kwargs={'analysis_id': results.Result.analysis_id}),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, results.Result.center_name)
        self.assertNotContains(response, 'Collapse all')
        self.assertNotContains(response, 'Expand all')
        self.assertContains(response, 'Show metadata XML')
        # test if response contains some of needed fields
        self.assertContains(response, 'Modified')
        self.assertContains(response, 'Disease')
        self.assertContains(response, 'Disease Name')
        self.assertContains(response, 'Sample Accession')
        # test raw_xml
        self.assertTrue(response.context['raw_xml'])

    def test_save_filters_state(self):
        response = self.client.get('%s?q=%s' % (reverse('search_page'), self.query))
        self.assertEqual(
                self.client.cookies.get(settings.LAST_QUERY_COOKIE).value,
                'q=%s' % self.query)
        response = self.client.get(reverse('home_page'))
        self.assertRedirects(response, '%s?q=%s' % (reverse('search_page'), self.query))

    def test_save_limit_in_cookies(self):
        response = self.client.get(reverse('home_page'), follow=True)
        self.assertNotIn(settings.PAGINATOR_LIMIT_COOKIE, response.cookies)
        response = self.client.get('%s?limit=25' % reverse('home_page'), follow=True)
        self.assertEqual(response.cookies[settings.PAGINATOR_LIMIT_COOKIE].value, '25')


class UtilsTestCase(TestCase):
    IDS_IN_CART = ["4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6",
                   "4b2235d6-ffe9-4664-9170-d9d2013b395f"]
    FILES_IN_CART = {IDS_IN_CART[0]: {"state": "live"},
                     IDS_IN_CART[1]: {"state": "bad_data"}}

    def test_get_filters_string(self):
        res = get_filters_string({
                        'study': 'TGGA',
                        'center_name': 'BCM',
                        'bad_param': 'bad'})
        self.assertEqual(res, '&study=TGGA&center_name=BCM')

    def test_get_wsapi_settings(self):
        value = 'somesetting'
        key = WSAPI_SETTINGS_LIST[0]
        with self.settings(**{'WSAPI_%s' % key: value}):
            self.assertEqual(get_wsapi_settings()[key], value)

    def test_generate_task_id(self):
        test_data = [
            {
                'dict': {'some': 'dict', '1': 2},
                'result': '971bf776baa021181f4cc5cf2d621967'},
            {
                'dict': {'another': 'dict', '1': 2},
                'result': '971bf776baa021181f4cc5cf2d621967'},
            {
                'dict': {'another': 'dict', '1': 2, '123': 'Some text'},
                'result': 'b351d6f2c44247961e7b641e4c5dcb65'},
        ]
        for data in test_data:
            self.assertEqual(generate_task_id(**data['dict']), data['result'])

    def test_get_default_query(self):
        with self.settings(
            DEFAULT_FILTERS = {
                'study': ('phs000178', '*Other_Sequencing_Multiisolate'),
                'state': ('live',),
                'upload_date': '[NOW-7DAY+TO NOW]'}):
            self.assertEqual(
                get_default_query(),
                'upload_date=[NOW-7DAY TO NOW]&study=(phs000178 OR *Other_Sequencing_Multiisolate)&state=(live)')
        # if not existing filter keys
        with self.settings(
            DEFAULT_FILTERS = {
                'study': ('phs000178', 'bad_key'),
                'state': ('live',),
                'upload_date': '[NOW-7DAY TO NOW]'}):
            self.assertEqual(
                get_default_query(),
                'upload_date=[NOW-7DAY TO NOW]&study=(phs000178)&state=(live)')
        # empty filters
        with self.settings(
            DEFAULT_FILTERS = {}):
            self.assertEqual(
                get_default_query(),
                '')

    def test_is_task_done(self):
        task_id = 'some-id-0000'
        # not existed task
        self.assertTrue(is_task_done(task_id))
        task_state = TaskState.objects.create(
                                        state=states.STARTED,
                                        task_id=task_id,
                                        tstamp=timezone.now())
        # waiting
        self.assertFalse(is_task_done(task_id))
        task_state.state = states.FAILURE
        task_state.save()
        # task is done
        self.assertTrue(is_task_done(task_id))

    def test_decrease_start_date(self):
        TEST_DATA = {
            'last_modified=[NOW-60DAY TO NOW-56DAY]&state=(live)':
                    'last_modified=%5BNOW-61DAY%20TO%20NOW-56DAY%5D&state=(live)',
            'upload_date=[NOW-2MONTH TO NOW-1MONTH]&state=(live)':
                    'upload_date=%5BNOW-63DAY%20TO%20NOW-1MONTH%5D&state=(live)',
            'upload_date=[NOW-10DAY TO NOW-3DAY]&last_modified=[NOW-1YEAR TO NOW-3DAY]':
                    'upload_date=%5BNOW-11DAY%20TO%20NOW-3DAY%5D&last_modified=%5BNOW-367DAY%20TO%20NOW-3DAY%5D',
            'state=(live)': 'state=(live)',
            'last_modified=[]': 'last_modified=[]',
            'upload_date=%5BNOW-16DAY%20TO%20NOW-15DAY%5D&state=%28live%29':
                    'upload_date=%5BNOW-17DAY%20TO%20NOW-15DAY%5D&state=%28live%29'
        }

        for i in TEST_DATA:
            self.assertEqual(decrease_start_date(i), TEST_DATA[i])

    def test_xml_add_spaces(self):
        xml = """<ResultSet date="2013-11-06 09:24:56"><Hits>10</Hits><Result id="1"><analysis_id>ad5ae127-56d1-4419-9dc9-f9385c839b99</analysis_id><state>live</state><reason/><last_modified>2013-06-09T07:27:48Z</last_modified><upload_date>2013-06-09T06:51:41Z</upload_date></Result></ResultSet>"""
        result = ''
        for i in xml_add_spaces(xml, space=1, tab=2):
            result += i
        self.assertEqual(result, """\n <ResultSet date="2013-11-06 09:24:56">\n   <Hits>10</Hits>\n   <Result id="1">\n     <analysis_id>ad5ae127-56d1-4419-9dc9-f9385c839b99</analysis_id>\n     <state>live</state>\n     <reason/>\n     <last_modified>2013-06-09T07:27:48Z</last_modified>\n     <upload_date>2013-06-09T06:51:41Z</upload_date>\n   </Result>\n </ResultSet>\n """)

    def test_paginator_params(self):
        url = reverse('home_page')
        request = get_request(url=url)
        self.assertEqual(paginator_params(request), (0, 10))
        request.COOKIES[settings.PAGINATOR_LIMIT_COOKIE] = 25
        self.assertEqual(paginator_params(request), (0, 25))
        request = get_request(url=url + '?offset=10')
        self.assertEqual(paginator_params(request), (10, 10))
        request = get_request(url=url + '?limit=50')
        self.assertEqual(paginator_params(request), (0, 50))


class ContextProcessorsTestCase(TestCase):

    def test_settings(self):
        # test cghub.apps.core.context_processors.settings
        MANY_FILES = 101
        with self.settings(MANY_FILES=MANY_FILES):
            factory = RequestFactory()
            request = factory.get('/')
            context = RequestContext(request)
            self.assertEqual(context['MANY_FILES'], MANY_FILES)


class TemplateTagsTestCase(TestCase):

    def test_sort_link_tag(self):
        test_request = HttpRequest()
        test_request.path = '/any_path/'
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(
            out,
            '<a class="sort-link" href="/any_path/?sort_by=last_modified" '
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
            'title="click to sort by Date Uploaded">Date Uploaded&nbsp;&darr;</a>')

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
            '<b>Text query</b>: "Some text"</li>'
            '<li data-name="center_name" data-filters="HMS-RK"><b>Center</b>: <span>HMS-RK </span></li>'
            '<li data-name="refassem_short_name" data-filters="HG18"><b>Assembly</b>: <span>HG18 </span></li>'
            '<li data-name="last_modified" data-filters="[NOW-7DAY TO NOW]"><b>Modified</b>: last week</li>'
            '<li data-name="disease_abbr" data-filters="CNTL&amp;COAD"><b>Disease</b>: <span>Controls (CNTL)</span>, <span>Colon adenocarcinoma (COAD)</span></li>'
            '<li data-name="study" data-filters="phs000178"><b>Study</b>: <span>TCGA (phs000178)</span></li>'
            '<li data-name="library_strategy" data-filters="WGS&amp;WXS"><b>Library Type</b>: <span>WGS </span>, <span>WXS </span></li></ul>')

    def test_items_per_page_tag(self):
        request = HttpRequest()
        default_limit = settings.DEFAULT_PAGINATOR_LIMIT
        default_limit_link = ('<a href="?limit={limit}"><span class="hidden">'
                'view </span>{limit}'.format(limit=default_limit))

        request.GET = QueryDict('', mutable=False)
        template = Template(
                "{% load pagination_tags %}{% items_per_page request " +
                str(default_limit) + " 100 %}")
        result = template.render(RequestContext(request, {}))
        self.assertIn('<a href="?limit=100"><span class="hidden">view </span>100', result)
        self.assertTrue(not default_limit_link in result)

        request.GET = QueryDict('limit=100', mutable=False)
        result = template.render(RequestContext(request, {}))
        self.assertTrue(not '<a href="?limit=100" '
                    'title="View 100 items per page">100</a>' in result)
        self.assertTrue(default_limit_link in result)

        template = Template(
            "{% load pagination_tags %}{% items_per_page request 10 'incorrect_data' %}")
        try:
            result = template.render(RequestContext(request, {}))
            assert 'No exception raised for incorrect data'
        except Exception as e:
            self.assertEqual(
                e.message,
                "Limits can be numbers or it's string representation")

    def test_get_name_by_code_tag(self):
        for section, section_data in ALL_FILTERS.iteritems():
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
        def value_resolver(value):
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
        def value_resolver(value):
            return right_value
        with self.settings(VALUE_RESOLVERS={'Study': value_resolver}):
            res = table_row(RESULT)
            self.assertIn(right_value, res)
            self.assertNotIn(RESULT['study'], res)

    def test_period_from_query(self):
        test_data = (
            {
                'query': '[NOW-2DAY TO NOW]',
                'result': '2013/02/25 - 2013/02/27'},
            { # test with quoted
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


class SearchViewPaginationTestCase(WithCacheTestCase):

    cart_cache_files = []
    wsapi_cache_files = [
        'd35ccea87328742e26a8702dee596ee9.xml',
        '6cc087ba392e318a84f3d1d261863728.ids',
    ]
    query = "6d54"

    def test_pagination_default_pagination(self):
        response = self.client.get(reverse('search_page') +
                                   '?q={query}&offset={offset}&limit={limit}'.format(
                                       query=self.query, offset=None, limit=None))
        self.assertContains(response, '1')
        self.assertContains(response, '2')
        self.assertContains(response, 'Prev')
        self.assertContains(response, 'Next')

    def test_pagination_one_page_limit_pagination(self):
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
        response = self.client.get(reverse('search_page') +
                                   '?q={query}&offset={offset}&limit={limit}'.format(
                                       query=self.query, offset=0, limit=1))
        self.assertContains(response, 'active')
        self.assertContains(response, 'Prev')
        self.assertContains(response, 'Next')

    def test_redirect_from_home_page(self):
        """
        Test redirect from home page if any GET parameters are specified.
        """
        response = self.client.get(
            reverse('home_page') + '?q={query}'.format(query=self.query),
            follow=True)
        self.assertTrue('search' in response.redirect_chain[0][0])


class PaginatorUnitTestCase(TestCase):

    def test_get_first_method(self):
        request = HttpRequest()
        paginator = Paginator({'num_results': 100, 'request': request})
        self.assertEqual(
            paginator.get_first(),
            {'url': '?offset=0&limit=10', 'page_number': 0}
        )

    def test_get_last_method(self):
        request = HttpRequest()
        paginator = Paginator({'num_results': 100, 'request': request})
        self.assertEqual(
            paginator.get_last(),
            {'url': '?offset=90&limit=10', 'page_number': 9}
        )


class MetadataViewTestCase(WithCacheTestCase):

    cart_cache_files = ['7b9cd36a-8cbb-4e25-9c08-d62099c15ba1']
    wsapi_cache_files = ['604f183c90858a9d1f1959fe0370c45d.xml']

    """
    Cached files will be used
    7b9cd36a-8cbb-4e25-9c08-d62099c15ba1 - 2012-10-29T21:56:12Z
    """
    analysis_id = '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1'
    last_modified = '2013-05-16T20:50:58Z'

    def test_metadata(self):
        path = os.path.join(settings.CART_CACHE_DIR, self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        response = self.client.get(
                    reverse('metadata',
                    args=[self.analysis_id]),
                    {'last_modified': self.last_modified, 'state': 'live'})
        content = response.content
        self.assertTrue(self.analysis_id in content)
        self.assertEqual(response['Content-Type'], 'text/xml')
        self.assertIn('attachment; filename=metadata.xml', response['Content-Disposition'])
        if os.path.isdir(path):
            shutil.rmtree(path)


class TaskViewsTestCase(TestCase):

    def test_celery_task_status(self):
        task_id = 'someid'

        def get_response():
            response = self.client.get(
                                reverse('celery_task_status'),
                                {'task_id': task_id},
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            return json.loads(response.content)

        response = self.client.get(reverse('celery_task_status'))
        self.assertEqual(response.status_code, 404)
        data = get_response()
        self.assertEqual(data['status'], 'failure')
        task_state = TaskState.objects.create(
                                        state=states.SUCCESS,
                                        task_id=task_id,
                                        tstamp=timezone.now())
        data = get_response()
        self.assertEqual(data['status'], 'success')
        task_state.state = states.FAILURE
        task_state.save()
        data = get_response()
        self.assertEqual(data['status'], 'failure')


class SettingsTestCase(TestCase):

    def test_table_columns_and_details_fields(self):
        """
        Check that all names from
        settings.TABLE_COLUMNS and
        settings.DETAILS_FILEDS exists
        """
        FILE_NAME = '871693661c3a3ed7898913da0de0c952.xml'

        from cghub.apps.core.attributes import COLUMN_NAMES
        from cghub.apps.core.templatetags.search_tags import field_values
        names = list(settings.TABLE_COLUMNS)
        for name in names:
            self.assertIn(name, COLUMN_NAMES)
        for name in settings.DETAILS_FIELDS:
            if name not in names:
                names.append(name)
        result = Results.from_file(
                        os.path.join(TEST_DATA_DIR, FILE_NAME),
                        get_wsapi_settings())
        result.add_custom_fields()
        field_values_dict = field_values(result.Result)
        for name in names:
            self.assertIn(name, field_values_dict)


class ErrorViewsTestCase(TestCase):

    def test_error_500(self):
        factory = RequestFactory()
        request = factory.get('/')
        r = error_500(request)
        self.assertEqual(r.status_code, 500)
        self.assertTrue(str(r).find('Server error.') != -1)
        with patch.object(sys, 'exc_info', return_value=(URLError, 'some val', 'some_tb')) as mock_exc_info:
            r = error_500(request)
            self.assertEqual(r.status_code, 500)
            self.assertTrue(str(r).find('Connection to WS-API server failed') != -1)

    def urlopen_mock(url):
            raise urllib2.URLError('Connection error')

    @patch('urllib2.urlopen', urlopen_mock)
    def test_status_500_if_urlopen_exception(self):
        """
        User should be notified in case of error occured in cghub.wsapi.utils.urlopen 
        """
        was_exception = False
        try:
            r = self.client.get(reverse('home_page'))
        except urllib2.URLError as e:
            was_exception = True
            self.assertIn('No response after', str(e))
        except:
            assert False, 'Enother exception than URLError raised'
        self.assertTrue(was_exception)

    @patch('urllib2.urlopen', urlopen_mock)
    def test_cart_add_files_return_error_if_urlopen_exception(self):
        # remove existing cache
        # filters = '{"analyte_code":"(D)"}'
        # cache file name = 2faab3400e367605bcf65cd3df490466.ids
        path = os.path.join(
                    settings.WSAPI_CACHE_DIR,
                    '2faab3400e367605bcf65cd3df490466.ids')
        if os.path.exists(path):
            os.remove(path)
        # create right request
        request = get_request(url=reverse(
                    'cart_add_remove_files', kwargs={'action': 'add'}))
        request.POST = {}
        request.POST['filters'] = '{"analyte_code":"(D)"}'
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = cart_add_files(request)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['action'], 'error')
