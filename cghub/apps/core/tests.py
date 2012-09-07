from django.core.urlresolvers import reverse
from lxml import objectify
import os
import shutil
from django.test.testcases import TestCase
from django.template import Template, Context, RequestContext
from django.http import HttpRequest
from wsapi.settings import CACHE_DIR


class CoreTests(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_non_existent_search(self):
        response = self.client.get('/search/?q=non_existent_search_query')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No results found' in response.content)

    def test_existent_search(self):
        response = self.client.get('/search/?q=6d7*')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Found' in response.content)


class TestTemplateTags(TestCase):
    def test_sort_link_tag(self):
        test_request = HttpRequest()
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(out,
            '<a href="/search/?sort_by=last_modified">Date Uploaded</a>')

        # make sure that other request.GET variables are preserved
        test_request.GET.update({'q': 'sample_query'})
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(out,
            '<a href="/search/?q=sample_query&amp;sort_by=last_modified">Date Uploaded</a>')

        # make sure that direction label is rendered if it is active sort filter
        del(test_request.GET['q'])
        test_request.GET.update({'sort_by': 'last_modified'})
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))

        self.assertEqual(out,
            '<a href="/search/?sort_by=-last_modified">Date Uploaded ASC</a>')

    def test_apllied_filters_tag(self):
        request = HttpRequest()
        request.GET.update({
            'center_name': '(HMS-RK)',
            'library_strategy': '(AMPLICON OR CTS)',
            'last_modified': '[NOW-7DAY TO NOW]',
            'disease_abbr': '(CNTL OR SARC)',
            })
        template = Template("{% load search_tags %}{% applied_filters request %}")
        result = template.render(RequestContext(request, {}))
        self.assertEqual(result, 'Applied filter(s):<p>- Center: Harvard;</p><p>- Upoladed this week;\
</p><p>- Disease: Controls, Sarcoma;</p><p>- Run Type: AMPLICON, CTS;</p>')

class SearchViewPaginationTestCase(TestCase):
    cache_files = [
        '24e93b68dff426925e6c0c65fc78958e.xml'
    ]
    query = "6d5*"

    def setUp(self):
        """
        Copy cached files to default cache directory.
        """

        # cache filenames are generated as following:
        # >>> m = hashlib.md5()
        # >>> m.update('xml_text=6d5%2A')
        # %2A - *
        # >>> m.hexdigest()
        # '24e93b68dff426925e6c0c65fc78958e'

        TEST_DATA_DIR = 'cghub/test_data/'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for f in self.cache_files:
            shutil.copy(
                os.path.join(TEST_DATA_DIR, f),
                os.path.join(CACHE_DIR, f)
            )
        self.default_results = objectify.fromstring(open(os.path.join(CACHE_DIR, self.cache_files[0])).read())
        self.default_results_count = len(self.default_results.findall('Result'))

    def test_pagination_default_pagination(self):
        response = self.client.get(reverse('search_page') +
                                   '?q={query}&offset={offset}&limit={limit}'.format(
                                       query=self.query, offset=None, limit=None))
        self.assertContains(response, '1')
        self.assertContains(response, '2')
        self.assertContains(response, 'Prev')
        self.assertContains(response, 'Next')

    def test_pagination_one_page_limit_pagination(self):
        response = self.client.get(reverse('search_page') +
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
                reverse('home_page')+'?q={query}'.format(query=self.query),
                follow=True)
        self.assertTrue('search' in response.redirect_chain[0][0])

    def test_last_modified_if_no_q(self):
        """
        Test that if there is not q query, last_modified is substituted.
        Search with last 7 days.
        """
        response = self.client.get(
                reverse('search_page')+
                    '?center_name={center_name}'.format(center_name='%28BCM%29'),
                follow=True)
        self.assertTrue('last_modified' in response.redirect_chain[0][0])
        self.assertTrue('7DAY' in response.redirect_chain[0][0])
