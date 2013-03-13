import os
import shutil
import contextlib
import datetime
from lxml import objectify
from mock import patch

from django.conf import settings
from django.utils import simplejson as json
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.template import Template, Context, RequestContext
from django.http import HttpRequest, QueryDict

from apps.core.templatetags.pagination_tags import Paginator

from cghub.apps.core.templatetags.search_tags import (get_name_by_code,
                    table_header, table_row, file_size, details_table,
                    period_from_query)
from cghub.apps.core.utils import (WSAPI_SETTINGS_LIST, get_filters_string,
                    get_wsapi_settings, generate_task_uuid,
                    manifest, metadata)
from cghub.apps.core.filters_storage import ALL_FILTERS


class WithCacheTestCase(TestCase):

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        # cache filenames are generated as following:
        # >>> from wsapi.cache import get_cache_file_name
        # >>> get_cache_file_name('xml_text=6d5%2A', True)
        # u'/tmp/wsapi/427dcd2c78d4be27efe3d0cde008b1f9.xml'

        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(settings.WSAPI_CACHE_DIR):
            os.makedirs(settings.WSAPI_CACHE_DIR)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(settings.WSAPI_CACHE_DIR, f)
            )
        self.default_results = objectify.fromstring(
            open(os.path.join(settings.WSAPI_CACHE_DIR, self.cache_files[0])).read())
        self.default_results_count = len(self.default_results.findall('Result'))

    def tearDown(self):
        for f in self.cache_files:
            os.remove(os.path.join(settings.WSAPI_CACHE_DIR, f))


class CoreTestCase(WithCacheTestCase):

    cache_files = [
        'd35ccea87328742e26a8702dee596ee9.xml',
        '35d58c85ed93322dcaacadef5538a455.xml',
        '5c4840476e9f1638af7e4ba9224c8689.xml',
        '871693661c3a3ed7898913da0de0c952.xml',
        '9824a6de49af620ba53c45c13ceccef0.xml',
        '9ff0ad7159cf4c2c360cc8070576e08a.xml',
        'aad96e9a8702634a40528d6280187da7.xml',
        '34a5eed3bc34ef7db3c91e9b72fce3b1.xml',
        '28e1cf619d26bdab58fcab5e7a2b9e6c.xml',
    ]
    query = "6d54*"

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_non_existent_search(self):
        response = self.client.get('/search/?q=non_existent_search_query')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No results found' in response.content)

    def test_existent_search(self):
        response = self.client.get('/search/?q=%s' % self.query)
        self.assertEqual(response.status_code, 200)

    def test_double_digit_for_sample_type(self):
        from lxml.html import fromstring
        response = self.client.get('/search/?q=%s' % self.query)
        c = fromstring(response.content)
        sample_type_index = 0
        for th in c.cssselect('th'):
            if th.cssselect('a'):
                if 'Sample Type' in th.cssselect('a')[0].text:
                    break
            sample_type_index += 1
        for tr in c.cssselect('tr'):
            sample_type = tr[sample_type_index].text
            if sample_type:
                self.assertTrue(len(sample_type) == 2)
        self.assertTrue('Found' in response.content)

    def test_item_details_view(self):
        uuid = '12345678-1234-1234-1234-123456789abc'
        response = self.client.get(reverse('item_details', kwargs={'uuid': uuid}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'No data.')

        from cghub.wsapi.api import request as api_request
        file_name = os.path.join(settings.WSAPI_CACHE_DIR, self.cache_files[0])
        results = api_request(file_name=file_name)
        self.assertTrue(hasattr(results, 'Result'))
        response = self.client.get(
                        reverse('item_details',
                        kwargs={'uuid': results.Result.analysis_id}))
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
                        kwargs={'uuid': results.Result.analysis_id}),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, results.Result.center_name)
        self.assertNotContains(response, 'Collapse all')
        self.assertNotContains(response, 'Expand all')
        self.assertContains(response, 'Show metadata XML')
        # test if response contains some of needed fields
        self.assertContains(response, 'Last modified')
        self.assertContains(response, 'Disease abbr')
        self.assertContains(response, 'Disease Name')
        self.assertContains(response, 'Sample Accession')
        # test raw_xml
        self.assertTrue(response.context['raw_xml'])


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

    def test_generate_task_uuid(self):
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
            self.assertEqual(generate_task_uuid(**data['dict']), data['result'])

    def test_manifest_xml(self):
        response = manifest(self.FILES_IN_CART, format='xml')
        man = response.content
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.IDS_IN_CART[0] in man)
        self.assertFalse(self.IDS_IN_CART[1] in man)
        self._check_content_type_and_disposition(response, type='text/xml', filename='manifest.xml')

    def test_manifest_tsv(self):
        response = manifest(self.FILES_IN_CART, format='tsv')
        man = response.content
        self.assertTrue(self.IDS_IN_CART[0] in man)
        self.assertFalse(self.IDS_IN_CART[1] in man)
        self._check_content_type_and_disposition(response, type='text/tsv', filename='manifest.tsv')

    def test_metadata_xml(self):
        response = metadata(self.FILES_IN_CART, format='xml')
        met = response.content
        for id in self.IDS_IN_CART:
            self.assertTrue('<analysis_id>%s</analysis_id>' % id in met)
        self._check_content_type_and_disposition(response, type='text/xml', filename='metadata.xml')

    def test_metadata_tvs(self):
        response = metadata(self.FILES_IN_CART, format='tsv')
        met = response.content
        for id in self.IDS_IN_CART:
            self.assertTrue(id in met)
        self._check_content_type_and_disposition(response, type='text/tsv', filename='metadata.tsv')

    def _check_content_type_and_disposition(self, response, type, filename):
        self.assertEqual(response['Content-Type'], type)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=%s' % filename)


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
            '<a class="sort-link" href="/any_path/?sort_by=last_modified">Date Uploaded</a>')

        test_request.path = ''
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(
            out,
            '<a class="sort-link" href="/search/?sort_by=last_modified">Date Uploaded</a>')

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
            '<a class="sort-link" href="/search/?q=sample_query&amp;sort_by=last_modified">Date Uploaded</a>')

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
            '<a class="sort-link" href="/search/?sort_by=-last_modified">Date Uploaded&nbsp;&darr;</a>')

    def test_applied_filters_tag(self):
        request = HttpRequest()
        request.GET.update({
            'study': '(phs000178)',
            'center_name': '(HMS-RK)',
            'library_strategy': '(WGS OR WXS)',
            'last_modified': '[NOW-7DAY TO NOW]',
            'disease_abbr': '(CNTL OR COAD)',
            'q': 'Some text'})
        template = Template("{% load search_tags %}{% applied_filters request %}")
        result = template.render(RequestContext(request, {}))
        self.assertEqual(
            result,
            u'Applied filter(s): <ul><li data-name="q" data-filters="Some text">'
            '<b>Text query</b>: "Some text"</li>'
            '<li data-name="center_name" data-filters="HMS-RK">'
            '<b>Center</b>: Harvard (HMS-RK)</li>'
            '<li data-name="last_modified" data-filters="[NOW-7DAY TO NOW]">'
            '<b>Modified</b>: last week</li><li data-name="disease_abbr" data-filters="CNTL&COAD">'
            '<b>Disease</b>: Controls (CNTL), Colon adenocarcinoma (COAD)</li>'
            '<li data-name="study" data-filters="phs000178"><b>Study</b>: TCGA (phs000178)</li>'
            '<li data-name="library_strategy" data-filters="WGS&WXS">'
            '<b>Run Type</b>: WGS, WXS</li></ul>')

    def test_items_per_page_tag(self):
        request = HttpRequest()
        default_limit = settings.DEFAULT_PAGINATOR_LIMIT
        default_limit_link = '<a href="?limit=%d">%d</a>' % (default_limit, default_limit)

        request.GET = QueryDict('', mutable=False)
        template = Template(
            "{% load pagination_tags %}{% items_per_page request " +
            str(default_limit) + " 100 %}")
        result = template.render(RequestContext(request, {}))
        self.assertTrue('<a href="?limit=100">100</a>' in result)
        self.assertTrue(not default_limit_link in result)
        
        request.GET = QueryDict('limit=100', mutable=False)
        result = template.render(RequestContext(request, {}))
        self.assertTrue(not '<a href="?limit=100">100</a>' in result)
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
        self.assertEqual(file_size(123456), '120.56 KB')
        self.assertEqual(file_size(1234567), '1.18 MB')
        self.assertEqual(file_size(1234567890), '1.15 GB')

    def test_table_header_tag(self):
        COLUMNS = (('Disease', 'visible'), ('UUID', 'hidden'),
                                                ('Study', 'visible'))
        request = HttpRequest()
        with self.settings(TABLE_COLUMNS = COLUMNS[:2]):
            res = table_header(request)
            self.assertTrue(res.find('<th') != -1)
            self.assertTrue(res.find(COLUMNS[0][0]) != -1)
            self.assertTrue(res.find(COLUMNS[1][0]) != -1)
            self.assertTrue(res.find('visible') != -1)
            self.assertTrue(res.find('hidden') != -1)
            self.assertTrue(res.find(COLUMNS[2][0]) == -1)

    def test_table_row_tag(self):
        COLUMNS = (('Disease', 'visible'), ('UUID', 'visible'),
                                                ('Study', 'visible'))
        RESULT = {
                'disease_abbr': 'COAD',
                'analysis_id': '6cca55c6-3748-4c05-8a31-0b1a125b39f5',
                'study': 'phs000178',
                }
        with self.settings(TABLE_COLUMNS = COLUMNS[:2]):
            res = table_row(RESULT)
            self.assertTrue(res.find('<td') != -1)
            self.assertTrue(res.find(RESULT['disease_abbr']) != -1)
            self.assertTrue(res.find(RESULT['analysis_id']) != -1)
            self.assertTrue(res.find(RESULT['study']) == -1)
        # test value_resolvers
        right_value = 'Right value'
        def value_resolver(value):
            return right_value
        with self.settings(VALUE_RESOLVERS={'Study': value_resolver}):
            res = table_row(RESULT)
            self.assertIn(right_value, res)
            self.assertNotIn(RESULT['study'], res)

    def test_details_table_tag(self):
        FIELDS = ('UUID', 'Study')
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


class SearchViewPaginationTestCase(WithCacheTestCase):

    cache_files = [
        'd35ccea87328742e26a8702dee596ee9.xml'
    ]
    query = "6d54*"

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

    def test_last_modified_if_no_q(self):
        """
        Test that if there is not q query, last_modified is substituted.
        Search with last month.
        """
        response = self.client.get(reverse('search_page'), follow=True)
        self.assertTrue('upload_date' in response.redirect_chain[0][0])
        self.assertTrue('7DAY' in response.redirect_chain[0][0])


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


class MetadataViewTestCase(TestCase):
    ID_DETAILS = "4b2235d6-ffe9-4664-9170-d9d2013b395f"

    def test_metadata(self):
        response = self.client.post(reverse('metadata', args=[self.ID_DETAILS]))
        metadata = response.content
        self.assertTrue(self.ID_DETAILS in metadata)
        self.assertEqual(response['Content-Type'], 'text/xml')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=metadata.xml')
