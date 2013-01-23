import os
import shutil
from lxml import objectify

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.template import Template, Context, RequestContext
from django.http import HttpRequest, QueryDict

from wsapi.settings import CACHE_DIR
from apps.core.templatetags.pagination_tags import Paginator

from cghub.apps.core.templatetags.search_tags import get_name_by_code
from cghub.apps.core.templatetags.core_tags import file_size
from cghub.apps.core.filters_storage import ALL_FILTERS


class CoreTests(TestCase):
    cache_files = [
        'd35ccea87328742e26a8702dee596ee9.xml'
    ]
    query = "6d54*"

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        # cache filenames are generated as following:
        # >>> from wsapi.cache import get_cache_file_name
        # >>> get_cache_file_name('xml_text=6d5%2A', True)
        # u'/tmp/wsapi/427dcd2c78d4be27efe3d0cde008b1f9.xml'

        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(CACHE_DIR, f)
            )
        self.default_results = objectify.fromstring(
            open(os.path.join(CACHE_DIR, self.cache_files[0])).read())
        self.default_results_count = len(self.default_results.findall('Result'))

    def tearDown(self):
        for f in self.cache_files:
            os.remove(os.path.join(CACHE_DIR, f))

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

    def test_item_datils_view(self):
        uuid = '12345678-1234-1234-1234-123456789abc'
        r = self.client.get(reverse('item_details', kwargs={'uuid': uuid}))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, u'No data.')

        from cghub.wsapi.api import request as api_request
        file_name = os.path.join(CACHE_DIR, self.cache_files[0])
        results = api_request(file_name=file_name)
        self.assertTrue(hasattr(results, 'Result'))
        r = self.client.get(
                        reverse('item_details',
                        kwargs={'uuid': results.Result.analysis_id}))
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, u'No data.')
        self.assertContains(r, results.Result.center_name)
        # not ajax
        self.assertContains(r, '<head>')
        # try ajax request
        r = self.client.get(
                        reverse('item_details',
                        kwargs={'uuid': results.Result.analysis_id}),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, results.Result.center_name)
        self.assertNotContains(r, '<head>')
        # test raw_xml
        self.assertTrue(r.context.get('raw_xml', False))


class TestTemplateTags(TestCase):
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
            'disease_abbr': '(CNTL OR COAD)', })
        template = Template("{% load search_tags %}{% applied_filters request %}")
        result = template.render(RequestContext(request, {}))
        self.assertEqual(
            result,
            'Applied filter(s): <ul><li id="time-filter-applied" '
            'data="[NOW-7DAY TO NOW]"><b>Uploaded</b>: this week</li>'
            '<li><b>Disease</b>: Controls (CNTL), Colon adenocarcinoma (COAD)</li>'
            '<li><b>Center</b>: Harvard (HMS-RK)</li>'
            '<li><b>Study</b>: TCGA (phs000178)</li><li><b>Run Type</b>: WGS, WXS</li></ul>')

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
        self.assertEqual(file_size(123456), '123.46 KB')
        self.assertEqual(file_size(1234567), '1.23 MB')
        self.assertEqual(file_size(1234567890), '1.23 GB')


class SearchViewPaginationTestCase(TestCase):
    cache_files = [
        'd35ccea87328742e26a8702dee596ee9.xml'
    ]
    query = "6d54*"

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        # cache filenames are generated as following:
        # >>> from wsapi.cache import get_cache_file_name
        # >>> get_cache_file_name('xml_text=6d5%2A', True)
        # u'/tmp/wsapi/427dcd2c78d4be27efe3d0cde008b1f9.xml'

        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(CACHE_DIR, f)
            )
        self.default_results = objectify.fromstring(
            open(os.path.join(CACHE_DIR, self.cache_files[0])).read())
        self.default_results_count = len(self.default_results.findall('Result'))

    def tearDown(self):
        for f in self.cache_files:
            os.remove(os.path.join(CACHE_DIR, f))

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
        response = self.client.get(
            reverse('search_page') +
            '?center_name={center_name}'.format(center_name='%28BCM%29'),
            follow=True)
        self.assertTrue('last_modified' in response.redirect_chain[0][0])
        self.assertTrue('1MONTH' in response.redirect_chain[0][0])


class PaginatorUnitTestCase(TestCase):
    def test_get_first_method(self):
        request = HttpRequest()
        paginator = Paginator({'num_results': 100, 'request': request})
        self.assertEqual(
            paginator.get_first(),
            {'url': '?&offset=0&limit=10', 'page_number': 0}
        )

    def test_get_last_method(self):
        request = HttpRequest()
        paginator = Paginator({'num_results': 100, 'request': request})
        self.assertEqual(
            paginator.get_last(),
            {'url': '?&offset=90&limit=10', 'page_number': 9}
        )
