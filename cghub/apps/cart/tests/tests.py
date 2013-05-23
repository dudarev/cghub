import os
import glob
import shutil
import datetime
import shutil

from celery import states
from djcelery.models import TaskState

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.utils import timezone
from django.utils.importlib import import_module
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

from cghub.settings.utils import PROJECT_ROOT

from cghub.apps.cart.utils import (manifest, metadata,
                            summary, add_ids_to_cart, add_files_to_cart,
                            load_missing_attributes, cache_file,
                            analysis_xml_iterator, summary_tsv_iterator,
                            cart_remove_files_without_attributes)
from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.cache import (AnalysisFileException, get_cart_cache_file_path, 
                    save_to_cart_cache, get_analysis_path, get_analysis,
                    get_analysis_xml, is_cart_cache_exists)
from cghub.apps.cart.parsers import parse_cart_attributes
from cghub.apps.cart.tasks import cache_results_task

from cghub.apps.core.tests import WithCacheTestCase, TEST_DATA_DIR, get_request
from cghub.apps.core.utils import generate_task_id

from cghub.wsapi.api import request as api_request
from cghub.wsapi import browser_text_search


def add_files_to_cart_dict(ids, selected_files=None):
    if not selected_files:
        selected_files = ids
    return {'selected_files': selected_files,
            'attributes': '{{"{0}":{{"analysis_id":"{0}", "files_size": 1048576, '
                '"state": "live", "last_modified": "2012-10-29T21:56:12Z"}},'
                '"{1}":{{"analysis_id":"{1}", "files_size": 1048576, '
                '"state": "live", "last_modified": "2012-10-29T21:56:12Z"}},'
                '"{2}":{{"analysis_id":"{2}", "files_size": 1048576, '
                '"state": "bad_data", "last_modified": "2012-10-29T21:56:12Z"}}}}'.format(*ids)}


class CartTestCase(TestCase):
    RANDOM_IDS = ('12345678-1234-1234-1234-123456789abc',
                  '12345678-4321-1234-1234-123456789abc',
                  '87654321-1234-1234-1234-123456789abc')

    def setUp(self):
        self.client = Client()
        self.cart_page_url = reverse('cart_page')

    def create_session(self):
        # FIXME: make this helper common common
        # initialize session
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        # create session
        s = Session(
                expire_date=timezone.now() + datetime.timedelta(days=7),
                session_key=store.session_key)
        s.save()

    def test_cart_add_files(self):
        url = reverse('cart_add_remove_files', args=['add'])

        self.client.post(url, add_files_to_cart_dict(ids=self.RANDOM_IDS),
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)

        # make sure counter in header is OK
        self.assertContains(response, 'Cart (3)')
        self.assertContains(response, 'Files in your cart: 3')

        # make sure we have 3 files in cart
        self.assertEqual(len(response.context['results']), 3)

        # make sure we have files we've posted
        for f in self.RANDOM_IDS:
            self.assertEqual(f in response.content, True)

    def test_card_add_duplicate_files(self):
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url,
                         add_files_to_cart_dict(
                             ids=self.RANDOM_IDS,
                             selected_files=[self.RANDOM_IDS[0], self.RANDOM_IDS[0],
                                                        self.RANDOM_IDS[0]]
                         ),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)

        # make sure we have only 1 file in cart
        self.assertEqual(len(response.context['results']), 1)

        # make sure counter in header is OK
        self.assertContains(response, 'Cart (1)')
        self.assertContains(response, 'Files in your cart: 1')

    def test_cart_remove_files(self):
        # add files
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url, add_files_to_cart_dict(ids=self.RANDOM_IDS),
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # remove files
        rm_selected_files = [self.RANDOM_IDS[0], self.RANDOM_IDS[1]]
        url = reverse('cart_add_remove_files', args=['remove'])
        self.client.post(url, {'selected_files': rm_selected_files},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(len(response.context['results']), 1)

        # make sure counter in header is OK
        self.assertContains(response, 'Cart (1)')
        self.assertContains(response, 'Files in your cart: 1')

        # make sure we do not have removed files in cart
        for f in rm_selected_files:
            self.assertEqual(f in response.content, False)

        # test removing doesn't loses sorting
        rm_selected_files = [self.RANDOM_IDS[2]]
        params = '?sort_by=analysis_id'
        url = reverse('cart_add_remove_files', args=['remove']) + params
        response = self.client.post(
                    url,
                    {'selected_files': rm_selected_files},
                    **{'HTTP_REFERER':'http://somepage.com/%s' % params,
                    'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertRedirects(response, reverse('cart_page') + params)

    def test_cart_pagination(self):
        # add 3 files to cart
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url, add_files_to_cart_dict(ids=self.RANDOM_IDS),
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Items per page:')

        # 2 items per page
        response = self.client.get(reverse('cart_page') +
                                   '?offset={offset}&limit={limit}'.format(
                                       offset=0, limit=2))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1')
        self.assertContains(response, '2')
        self.assertContains(response, 'Prev')
        self.assertContains(response, 'Next')
        self.assertContains(response, 'Items per page:')

        # 2 items per page, 2nd page
        response = self.client.get(reverse('cart_page') +
                                   '?offset={offset}&limit={limit}'.format(
                                       offset=2, limit=2))
        self.assertEqual(response.status_code, 200)

    def test_cart_add_raise_http_404_when_get(self):
        """
        Only POST method allowed for 'cart_add_remove_files' url
        """
        url = reverse('cart_add_remove_files', args=['add'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_cart_view_not_modified_session(self):
        """
        This cause problems when view makes more recent changes in session
        than task that adds files to cart.
        """
        self.create_session()
        self.assertNotIn('cart', self.client.session)
        url = reverse('cart_page')
        r = self.client.get(url)
        # check that session was not modified (cart not created)
        self.assertNotIn('cart', self.client.session)


class CartClearTestCase(TestCase):
    IDS_IN_CART = ('4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6',
                   '4b2235d6-ffe9-4664-9170-d9d2013b395f',
                   '7be92e1e-33b6-4d15-a868-59d5a513fca1')

    def setUp(self):
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url, add_files_to_cart_dict(ids=self.IDS_IN_CART),
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_clear_cart(self):
        url = reverse('clear_cart')
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Files in your cart: 0 (0 Bytes)")
        self.assertContains(response, "Your cart is empty!")


class CartAddItemsTestCase(TestCase):

    def create_session(self):
        # initialize session
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        # create session
        s = Session(
                expire_date=timezone.now() + datetime.timedelta(days=7),
                session_key=store.session_key)
        s.save()

    def test_cart_add_files_with_q(self):
        self.create_session()
        data = {
            'filters': json.dumps({
                        'state': '(live)',
                        'q': '(00b27c0f-acf5-434c-8efa-25b1f3c4f506)'
                    })}
        url = reverse('cart_add_remove_files', args=('add',))
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        if browser_text_search.useAllMetadataIndex:
            self.assertTrue(data['task_id'])
        else:
            self.assertNotIn('task_id', data)
        self.assertTrue(self.client.session.session_key)

    def test_cart_add_files_with_q_without_metadata_index(self):
        """
        with  cghub.wsapi.browser_text_search.useAllMetadataIndex = False
        """
        oldUseAllMetadataIndex = browser_text_search.useAllMetadataIndex
        browser_text_search.useAllMetadataIndex = False
        self.create_session()
        data = {
            'filters': json.dumps({
                    'state': '(live)',
                    'q': '(00b27c0f-acf5-434c-8efa-25b1f3c4f506)'
                })}
        url = reverse('cart_add_remove_files', args=('add',))
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        if browser_text_search.useAllMetadataIndex:
            self.assertTrue(data['task_id'])
        else:
            self.assertNotIn('task_id', data)
        self.assertTrue(self.client.session.session_key)
        browser_text_search.useAllMetadataIndex = oldUseAllMetadataIndex

    def test_add_files_without_q(self):
        self.create_session()
        data = {
            'filters': json.dumps({
                        'state': '(live)',
                        'upload_date': '[NOW-1DAY TO NOW]',
                        'study': '(*Other_Sequencing_Multiisolate)'
                    })}
        url = reverse('cart_add_remove_files', args=('add',))
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'redirect')
        self.assertTrue(data['task_id'])


class CartCacheTestCase(WithCacheTestCase):

    """
    Cached files will be used
    7b9cd36a-8cbb-4e25-9c08-d62099c15ba1 - 2013-05-16T20:50:58Z
    8cab937e-115f-4d0e-aa5f-9982768398c2 - 2013-04-27T01:47:09Z
    """
    analysis_id = '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1'
    last_modified = '2013-05-16T20:50:58Z'
    analysis_id2 = '8cab937e-115f-4d0e-aa5f-9982768398c2'
    last_modified2 = '2013-05-16T20:51:58Z'

    wsapi_cache_files = [
            '604f183c90858a9d1f1959fe0370c45d.xml',
            '833d652164e4317c6a01d17baca9297c.xml',
            '04431431d567221ad5cec406209e9d27.xml',
    ]
    cart_cache_files = [analysis_id, analysis_id2]

    def test_get_cache_file_path(self):
        self.assertEqual(
                get_cart_cache_file_path(
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                        '2012-10-29T21:56:12Z'),
                os.path.join(
                        settings.CART_CACHE_DIR,
                        '7b/9c/7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/2012-10-29T21:56:12Z/analysisFull.xml'))
        self.assertEqual(
                get_cart_cache_file_path(
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                        '2012-10-29T21:56:12Z',
                        short=True),
                os.path.join(
                        settings.CART_CACHE_DIR,
                        '7b/9c/7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/2012-10-29T21:56:12Z/analysisShort.xml'))

    def test_save_to_cart_cache(self):
        path = os.path.join(
                            settings.CART_CACHE_DIR,
                            self.analysis_id[:2],
                            self.analysis_id[2:4],
                            self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        path_full = get_cart_cache_file_path(self.analysis_id, self.last_modified)
        path_short = get_cart_cache_file_path(self.analysis_id, self.last_modified, short=True)
        # check is_cart_cache_exists
        self.assertFalse(is_cart_cache_exists(self.analysis_id, self.last_modified))
        result = save_to_cart_cache(self.analysis_id, self.last_modified)
        self.assertTrue(os.path.exists(path_full))
        self.assertTrue(os.path.exists(path_short))
        self.assertTrue(is_cart_cache_exists(self.analysis_id, self.last_modified))
        shutil.rmtree(path)
        # check exception raises when file does not exists
        bad_analysis_id = 'badanalysisid'
        path = os.path.join(
                    settings.CART_CACHE_DIR,
                    bad_analysis_id[:2],
                    bad_analysis_id[2:4],
                    bad_analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        try:
            save_to_cart_cache(bad_analysis_id, self.last_modified)
        except AnalysisFileException as e:
            self.assertEqual(unicode(e), 'File for analysis_id=badanalysisid, '
            'which was last modified 2013-05-16T20:50:58Z. '
            'File with specified analysis_id not found')
        else:
            raise False, 'AnalysisFileException doesn\'t raised'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check case when file was updated
        path = os.path.join(
                        settings.CART_CACHE_DIR,
                        self.analysis_id[:2],
                        self.analysis_id[2:4],
                        self.analysis_id)
        try:
            save_to_cart_cache(self.analysis_id, '1900-10-29T21:56:12Z')
        except AnalysisFileException:
            assert False, 'Most recent file was not downloaded'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check access denied to files outside cache dir
        try:
            save_to_cart_cache(self.analysis_id, '../../same_outside_dir')
        except AnalysisFileException as e:
            self.assertEqual(
                unicode(e),
                'File for analysis_id=7b9cd36a-8cbb-4e25-9c08-d62099c15ba1, '
                'which was last modified ../../same_outside_dir. '
                'Bad analysis_id or last_modified')
        else:
            raise False, 'AnalysisFileException doesn\'t raised'

    def test_cache_results_task(self):
        """
        Check that exception not rised when passed not existed analysis_id/last_modified pair
        """
        cache_results_task(self.analysis_id, '1900-10-29T21:56:12Z')

    def test_get_analysis(self):
        # test get_analysis_path
        path = os.path.join(
                            settings.CART_CACHE_DIR,
                            self.analysis_id[:2],
                            self.analysis_id[2:4],
                            self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        analysis_path = get_analysis_path(self.analysis_id, self.last_modified)
        self.assertEqual(
            analysis_path,
            get_cart_cache_file_path(self.analysis_id, self.last_modified))
        self.assertTrue(os.path.exists(analysis_path))
        # now using cache
        analysis_path = get_analysis_path(self.analysis_id, self.last_modified)
        self.assertEqual(
            analysis_path,
            get_cart_cache_file_path(self.analysis_id, self.last_modified))
        # test get_analysis
        # with cache
        analysis = get_analysis(self.analysis_id, self.last_modified, short=False)
        self.assertEqual(analysis.Hits, 1)
        content = analysis.tostring()
        self.assertIn('analysis_xml', content)
        # short version
        analysis = get_analysis(self.analysis_id, self.last_modified, short=True)
        content = analysis.tostring()
        self.assertNotIn('analysis_xml', content)
        self.assertEqual(analysis.Hits, 1)
        # without cache
        shutil.rmtree(path)
        analysis = get_analysis(self.analysis_id, self.last_modified)
        self.assertEqual(analysis.Hits, 1)

    def test_get_analysis_xml(self):
        xml, size = get_analysis_xml(
            analysis_id=self.analysis_id,
            last_modified=self.last_modified)
        self.assertNotIn('Result', xml)
        self.assertIn('analysis_id', xml)
        self.assertEqual(size, 172861573)

    def test_analysis_xml_iterator(self):
        data = {
            self.analysis_id: {'last_modified': self.last_modified, 'state': 'live'},
            self.analysis_id2: {'last_modified': self.last_modified2, 'state': 'live'}}
        iterator = analysis_xml_iterator(data)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('ResultSet', result)
        self.assertIn('Result id="1"', result)
        self.assertIn('Result id="2"', result)

    def test_summary_tsv_iterator(self):
        data = {
            self.analysis_id: {'last_modified': self.last_modified, 'state': 'live'},
            self.analysis_id2: {'last_modified': self.last_modified2, 'state': 'live'}}
        iterator = summary_tsv_iterator(data)
        result = ''
        for i in iterator:
            result += i
        self.assertIn('center', result)
        self.assertIn('analysis_id', result)
        self.assertIn(self.last_modified[:10], result)
        self.assertIn(self.analysis_id, result)
        self.assertIn(self.analysis_id2, result)

    def test_manifest(self):
        data = {
            self.analysis_id: {'last_modified': self.last_modified, 'state': 'live'},
            self.analysis_id2: {'last_modified': self.last_modified2, 'state': 'live'}}
        response = manifest(data)
        content = response.content
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id in content)
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id2 in content)
        self._check_content_type_and_disposition(response, type='text/xml', filename='manifest.xml')

    def test_metadata(self):
        data = {
            self.analysis_id: {'last_modified': self.last_modified, 'state': 'live'},
            self.analysis_id2: {'last_modified': self.last_modified2, 'state': 'live'}}
        response = metadata(data)
        content = response.content
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id in content)
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.analysis_id2 in content)
        self._check_content_type_and_disposition(response, type='text/xml', filename='metadata.xml')

    def test_summary(self):
        data = {
            self.analysis_id: {'last_modified': self.last_modified, 'state': 'live'},
            self.analysis_id2: {'last_modified': self.last_modified2, 'state': 'live'}}
        response = summary(data)
        content = response.content
        self.assertTrue(all(field.lower().replace(' ', '_') in content
                            for field in settings.TABLE_COLUMNS))
        self.assertTrue(self.analysis_id in content)
        self.assertTrue(self.analysis_id2 in content)
        self._check_content_type_and_disposition(response, type='text/tsv', filename='summary.tsv')

    def _check_content_type_and_disposition(self, response, type, filename):
        self.assertEqual(response['Content-Type'], type)
        self.assertIn('attachment; filename=%s' % filename, response['Content-Disposition'])

    def test_cache_file(self):
        # asinc == False
        # {CART_CACHE_DIR}/7b/9c/7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/ should be created
        path = os.path.join(
                            settings.CART_CACHE_DIR,
                            self.analysis_id[:2],
                            self.analysis_id[2:4],
                            self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        cache_file(
                analysis_id=self.analysis_id, last_modified=self.last_modified,
                asinc=False)
        self.assertTrue(os.path.isdir(path))
        shutil.rmtree(path)
        # asinc = True
        cache_file(
                analysis_id=self.analysis_id, last_modified=self.last_modified,
                asinc=True)
        self.assertTrue(os.path.isdir(path))
        shutil.rmtree(path)
        # asinc = True, and task already exists
        now = timezone.now()
        task_id = generate_task_id(
                analysis_id=self.analysis_id, last_modified=self.last_modified)
        ts = TaskState(
                    state=states.SUCCESS, task_id=task_id,
                    tstamp=now)
        ts.save()
        cache_file(
                analysis_id=self.analysis_id, last_modified=self.last_modified,
                asinc=True)
        self.assertFalse(os.path.isdir(path))
        # if task was created more than 5 days ago
        old_time = now - datetime.timedelta(days=7)
        ts.tstamp = old_time
        ts.save()
        cache_file(
                analysis_id=self.analysis_id, last_modified=self.last_modified,
                asinc=True)
        self.assertTrue(os.path.isdir(path))
        # check that tstamp was updated
        self.assertNotEqual(
                    TaskState.objects.get(task_id=task_id).tstamp,
                    old_time)


class CartParsersTestCase(TestCase):

    test_file = os.path.join(
                    os.path.dirname(__file__),
                    '../../../test_data/f1db42e28cca7a220508b4e9778f66fc.xml')

    def test_parse_cart_attributes(self):
        # initialize session
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        # create session
        s = Session(
                expire_date=timezone.now() + datetime.timedelta(days=7),
                session_key=store.session_key)
        s.save()
        # prefill cart by ids
        session = Session.objects.get(session_key=self.client.session.session_key)
        session_data = session.get_decoded()
        session_data['cart'] = {}
        session_data['cart']['5464f590-587a-4590-8145-f683410ec407'] = {'analysis_id': '5464f590-587a-4590-8145-f683410ec407'}
        session_data['cart']['ff258e70-4a00-45b4-bda9-9134b05c0319'] = {'analysis_id': 'ff258e70-4a00-45b4-bda9-9134b05c0319'}
        session.session_data = Session.objects.encode(session_data)
        session.save()
        attributes = ['study', 'center_name', 'analyte_code', 'last_modified',
                                        'assembly', 'files_size', 'analysis_id']
        session_store = SessionStore(session_key=self.client.session.session_key)
        parse_cart_attributes(session_store, attributes, file_path=self.test_file,
                                                    cache_files=False)
        # check task created
        session = Session.objects.get(session_key=self.client.session.session_key)
        session_data = session.get_decoded()
        # 5464f590-587a-4590-8145-f683410ec407 - 2012-05-10T06:23:39Z
        # ff258e70-4a00-45b4-bda9-9134b05c0319 - 2012-05-18T03:25:49Z
        self.assertEqual(
                    session_data['cart']['5464f590-587a-4590-8145-f683410ec407']['last_modified'],
                    '2012-05-10T06:23:39Z')
        self.assertTrue(session_data['cart']['5464f590-587a-4590-8145-f683410ec407']['study'])
        self.assertTrue(int(session_data['cart']['5464f590-587a-4590-8145-f683410ec407']['files_size']))
        self.assertEqual(
                    session_data['cart']['ff258e70-4a00-45b4-bda9-9134b05c0319']['last_modified'],
                    '2012-05-18T03:25:49Z')


class CartFormsTestCase(TestCase):

    def test_selected_files_form(self):

        test_data_set = [{
            'attributes': json.dumps({
                    '7850f073-642a-40a8-b49d-e328f27cfd66': {'study': 'TCGA', 'size': 10},
                    '796e11c8-b873-4c37-88cd-18dcd7f287ec': {'study': 'TCGA', 'size': 10}}),
            'is_valid': True,
            }, {
            'attributes': 123,
            'is_valid': False,
            }, {
            'attributes': json.dumps({'study': 'TCGA', 'size': 10}),
            'is_valid': False }]

        for data in test_data_set:
            form = SelectedFilesForm(data)
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = SelectedFilesForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['attributes']['7850f073-642a-40a8-b49d-e328f27cfd66'],
            {'study': 'TCGA', 'size': 10})

    def test_all_files_form(self):

        test_data_set = [{
            'filters': json.dumps({'center': '(1,2)', 'state': '(live)'}),
            'is_valid': True,
        }, {
            'filters': json.dumps(['bad', 'filters']),
            'is_valid': False,
        }]

        for data in test_data_set:
            form = AllFilesForm(data)
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = AllFilesForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['filters'],
            {'center': '(1,2)', 'state': '(live)'})


class CartUtilsTestCase(TestCase):

    def test_add_ids_to_cart(self):
        request = get_request()
        # try to add ids
        ids = (
            '7850f073-642a-40a8-b49d-e328f27cfd66',
            '796e11c8-b873-4c37-88cd-18dcd7f287ec')
        add_ids_to_cart(request, ids)
        # check ids saved to session
        self.assertEqual(
                request.session._session['cart'][
                    '7850f073-642a-40a8-b49d-e328f27cfd66']['analysis_id'],
                '7850f073-642a-40a8-b49d-e328f27cfd66')

    def test_load_missing_attributes(self):
        files = [
            {'analysis_id': '7850f073-642a-40a8-b49d-e328f27cfd66', 'study': 'live'},
            {'analysis_id': '796e11c8-b873-4c37-88cd-18dcd7f287ec'}]
        files = load_missing_attributes(files)
        # first is unchanged
        self.assertEqual(len(files[0]), 2)
        # attributes was loaded for second item
        self.assertEqual(files[1]['disease_abbr'], 'COAD')

    def test_cart_remove_files_without_attributes(self):
        request = get_request()
        request.session['cart'] = {
            '7850f073-642a-40a8-b49d-e328f27cfd66': {
                'analysis_id': '7850f073-642a-40a8-b49d-e328f27cfd66',
                'study': 'live',
                'last_modified': '2012-05-10T06:23:39Z'},
            '796e11c8-b873-4c37-88cd-18dcd7f287ec': {
                'analysis_id': '796e11c8-b873-4c37-88cd-18dcd7f287ec',
                'study': 'live',
                'last_modified': '2012-05-10T06:23:39Z'},
            '226e11c8-b873-4c37-88cd-18dcd7f28733': {
                'analysis_id': '226e11c8-b873-4c37-88cd-18dcd7f28733'},
            '116e11c8-b873-4c37-88cd-18dcd7f28744': {
                'analysis_id': '116e11c8-b873-4c37-88cd-18dcd7f28744'},
        }
        cart_remove_files_without_attributes(request)
        self.assertEqual(len(request.session._session['cart']), 2)
        self.assertIn(
                '7850f073-642a-40a8-b49d-e328f27cfd66',
                request.session._session['cart'])
        self.assertNotIn(
                '226e11c8-b873-4c37-88cd-18dcd7f28733',
                request.session._session['cart'])

    def test_add_files_to_cart(self):
        request = get_request()
        filename = os.path.join(TEST_DATA_DIR ,'d35ccea87328742e26a8702dee596ee9.xml')
        results = api_request(file_name=filename)
        results.add_custom_fields()
        add_files_to_cart(request, results)
        cart = request.session._session['cart']
        self.assertEqual(len(cart), 2)
        self.assertEqual(
                cart['80e7daa9-6a53-4e78-a0ad-7f46667438c5']['upload_date'],
                '2012-09-21T20:40:06Z')
