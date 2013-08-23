import os.path
import sys
import shutil
import datetime
import codecs

from urllib2 import URLError
from mock import patch
from cghub_python_api import SOLRRequest

from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.testcases import TestCase
from django.test.client import RequestFactory
from django.template import Template, Context, RequestContext
from django.http import HttpRequest, QueryDict
from django.utils.importlib import import_module
from django.contrib.sessions.models import Session

from cghub.apps.cart.utils import Cart

from ..templatetags.pagination_tags import Paginator
from ..templatetags.search_tags import (
                    get_name_by_code, table_header, table_row,
                    file_size, details_table, period_from_query,
                    only_date, get_sample_type_by_code)
from ..templatetags.core_tags import without_header
from ..utils import (
                    get_filters_dict, query_dict_to_str, xml_add_spaces,
                    paginator_params, generate_tmp_file_name,
                    get_results_for_ids)
from ..requests import (
                    RequestFull, RequestDetail, RequestID,
                    ResultFromSOLRFile, build_wsapi_xml)
from ..views import error_500
from ..filters_storage import ALL_FILTERS
from ..forms import BatchSearchForm, AnalysisIDsForm


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


class CoreTestCase(TestCase):

    query = "6d54"

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # check ajax urls is available
        self.assertContains(response, reverse('help_hint'))
        self.assertContains(response, reverse('help_text'))

    def test_non_existent_search(self):
        response = self.client.get('/search/?q=non_existent_search_query')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No results found' in response.content)

    def test_existent_search(self):
        response = self.client.get('/search/?q=%s' % self.query)
        self.assertEqual(response.status_code, 200)

    def test_item_details_view(self):
        analysis_id = '916d1bd2-f503-4775-951c-20ff19dfe409'
        bad_analysis_id = 'badd1bd2-f503-4775-951c-123456789112'
        response = self.client.get(reverse(
                'item_details', kwargs={'analysis_id': bad_analysis_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'No data.')

        api_request = RequestFull(query={'analysis_id': analysis_id})
        result = api_request.call().next()
        self.assertEqual(api_request.hits, 1)
        response = self.client.get(
                        reverse('item_details',
                        kwargs={'analysis_id': analysis_id}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, u'No data.')
        self.assertContains(response, result['center_name'])
        # not ajax
        self.assertContains(response, '<head>')
        self.assertContains(response, 'Collapse all')
        self.assertContains(response, 'Expand all')
        # try ajax request
        response = self.client.get(
                        reverse('item_details',
                        kwargs={'analysis_id': analysis_id}),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, result['center_name'])
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
        # check all entries are present
        self.assertIn('run_xml', response.context['raw_xml'])

    def test_save_filters_state(self):
        # TODO: Extend this test (only filters should be persistent, not query)
        response = self.client.get(
                '%s?q=%s' % (reverse('search_page'), self.query))
        self.assertEqual(
                self.client.cookies.get(settings.LAST_QUERY_COOKIE).value,
                'q=%s' % self.query)
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.query)

    def test_save_limit_in_cookies(self):
        DEFAULT_FILTERS = {
                'study': ('phs000178', '*Other_Sequencing_Multiisolate'),
                'state': ('live',),
                'upload_date': '[NOW-7DAY+TO+NOW]'}
        with self.settings(DEFAULT_FILTERS = DEFAULT_FILTERS):
            response = self.client.get(
                    '%s?%s' % (
                            reverse('search_page'),
                            query_dict_to_str(DEFAULT_FILTERS)))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                    response.cookies[settings.PAGINATOR_LIMIT_COOKIE].value,
                    str(settings.DEFAULT_PAGINATOR_LIMIT))
            response = self.client.get(
                    '%s?%s&limit=25' % (
                            reverse('search_page'),
                            query_dict_to_str(DEFAULT_FILTERS)))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.cookies[settings.PAGINATOR_LIMIT_COOKIE].value, '25')

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


class RequestsTestCase(TestCase):

    def clean_xml(self, xml):
        xml = xml.replace('\t', '').replace('\n', '')
        while xml.find('  ') != -1:
            xml = xml.replace('  ', ' ')
        xml = xml.replace('> <', '><')
        xml = u'%s%s' % (xml[0:72], xml[91:])
        # remove urls
        start = xml.find('<analysis_detail_uri>')
        stop = xml.find('</analysis_data_uri>')
        if start != -1 and stop != -1:
            xml = u'%s%s' % (xml[:start], xml[stop:])
        return xml

    def test_build_wsapi_xml(self):
        path_wsapi = os.path.join(
                os.path.dirname(__file__),
                'test_data/full_metadata_xml_wsapi.xml')
        path_solr = os.path.join(
                os.path.dirname(__file__),
                'test_data/full_metadata_xml_solr.xml')
        api_request = ResultFromSOLRFile(query={'filename': path_solr})
        result_solr = api_request.call().next()
        xml_solr =  build_wsapi_xml(result_solr)
        with codecs.open(path_wsapi, 'r', encoding='utf-8') as f:
            xml_wsapi = f.read()
        self.assertIn(settings.CGHUB_SERVER, xml_solr)
        xml_solr = self.clean_xml(xml_solr)
        xml_wsapi = self.clean_xml(xml_wsapi)
        self.assertEqual(xml_solr, xml_wsapi)


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
        # test sorting disabled on cart page
        test_request.path = reverse('cart_page')
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
        ).render(Context({
            'request': test_request
        }))
        self.assertEqual(
            out,
            '<a href="#" onclick="return false;">Date Uploaded</a>')

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


class BatchSearchTestCase(TestCase):

    def test_batch_search_form(self):
        ids = [
            '0005d2d0-aede-4f5c-89fa-aed12abfadd6',
            '00007994-abeb-4b16-a6ad-7230300a29e9',
            '000f332c-7fd9-4515-bf5f-9b77db43a3fd',
            '00007994-abeb-4b16-a6ad-7230300a29e9',
            'TCGA-04-1337-01A-01W-0484-10',
        ]
        f = SimpleUploadedFile(name='ids.csv', content=' '.join(ids))
        form = BatchSearchForm({'text': ' '.join(ids)})
        self.assertTrue(form.is_valid())
        form = BatchSearchForm({}, {'upload': f})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data['ids']), 3)
        self.assertEqual(len(form.cleaned_data['legacy_sample_ids']), 1)
        for id in ids:
            self.assertTrue(
                    (id in form.cleaned_data['ids']) or
                    (id in form.cleaned_data['legacy_sample_ids']))
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
        response = self.client.get(reverse('batch_search_page'))
        self.assertEqual(response.status_code, 200)
        # submit wrong data
        data = {'text': 'badtext'}
        response = self.client.post(reverse('batch_search_page'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No valid ids was found')
        # submit not existed analysis_id
        data = {
            'text': '0005d2d0-aede-4f5c-89fa-aed12abfadd6 '
            '00007994-abeb-4b16-a6ad-7230300a29e9 '
            'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'}
        response = self.client.post(reverse('batch_search_page'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Found by analysis_id: 2')
        # ok, adding files to cart
        ids = response.content
        ids = ids[ids.find('<textarea'):ids.find('</textarea>')]
        ids = ids[ids.find('>') + 1:]
        create_session(self)
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
