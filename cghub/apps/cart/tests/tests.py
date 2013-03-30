import os
import glob
import shutil
import datetime
import shutil

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.utils import timezone
from django.utils.importlib import import_module
from django.contrib.sessions.models import Session
from django.conf import settings

from cghub.settings.utils import PROJECT_ROOT
from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.cache import (AnalysisFileException, get_cart_cache_file_path, 
                    save_to_cart_cache, get_analysis_path, get_analysis,
                    join_analysises)

from cghub.apps.core.tests import WithCacheTestCase


def add_files_to_cart_dict(ids, selected_files=['file1', 'file2', 'file3']):
    return {'selected_files': selected_files,
            'attributes': '{"file1":{"analysis_id":"%s", "files_size": 1048576, "state": "live"},'
                           '"file2":{"analysis_id":"%s", "files_size": 1048576, "state": "live"},'
                           '"file3":{"analysis_id":"%s", "files_size": 1048576, "state": "bad_data"}}' % ids}


class CartTestCase(TestCase):
    RANDOM_IDS = ('12345678-1234-1234-1234-123456789abc',
                  '12345678-4321-1234-1234-123456789abc',
                  '87654321-1234-1234-1234-123456789abc')

    def setUp(self):
        self.client = Client()
        self.cart_page_url = reverse('cart_page')

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
        self.assertContains(response, '3.00 MB')

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
                             selected_files=['file1', 'file1', 'file1']
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


class ClearCartTestCase(TestCase):
    IDS_IN_CART = ('4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6',
                   '4b2235d6-ffe9-4664-9170-d9d2013b395f',
                   '7be92e1e-33b6-4d15-a868-59d5a513fca1')

    def setUp(self):
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url, add_files_to_cart_dict(ids=self.IDS_IN_CART),
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_clear_cart(self):
        url = reverse('clear_cart')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Files in your cart: 0 (0 Bytes)")
        self.assertContains(response, "Your cart is empty!")


class CartAddItemsTestCase(WithCacheTestCase):
    cache_files = [
        'c0fc7dd542430ce04e8c6e0d065cfd71.xml'
    ]

    def test_cart_add_files(self):
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
        data = {
            'attributes': json.dumps(['study', 'center_name', 'analyte_code']),
            'filters': json.dumps({
                        'state': '(live)',
                        'last_modified': '[NOW-1DAY TO NOW]',
                        'analyte_code': '(D)'})}
        url = reverse('cart_add_remove_files', args=('add',))
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['action'], 'message')
        self.assertTrue(data['task_id'])
        self.assertTrue(self.client.session.session_key)
        # check task created
        session = Session.objects.get(session_key=self.client.session.session_key)
        session_data = session.get_decoded()
        self.assertEqual(len(session_data['cart']), 14)

'''
class OldCacheTestCase(TestCase):
    IDS_IN_CART = ("4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6",
                   "4b2235d6-ffe9-4664-9170-d9d2013b395f",
                   "7be92e1e-33b6-4d15-a868-59d5a513fca1")
    def setUp(self):
        self.api_results_cache_dir = settings.CART_CACHE_DIR
        files = glob.glob(os.path.join(self.api_results_cache_dir, '*'))
        for file in files:
            if not os.path.isdir(file):
                os.remove(file)
        files = glob.glob(os.path.join(testdata_dir, '*'))
        for file in files:
            shutil.copy(file, os.path.join(self.api_results_cache_dir, os.path.basename(file)))

        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url, add_files_to_cart_dict(ids=self.IDS_IN_CART),
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def tearDown(self):
        files = glob.glob(os.path.join(self.api_results_cache_dir, '*'))
        for file in files:
            if not os.path.isdir(file):
                pass
                os.remove(file)

    # test for new cache functions TODO(nanvel): remove this comments and unnecessary tests
    def test_save_to_cache(self):
        """
        7b9cd36a-8cbb-4e25-9c08-d62099c15ba1 - 2012-10-29T21:56:12Z
        """
        analysis_id = '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1'
        last_modified = '2012-10-29T21:56:12Z'
        path = os.path.join(settings.CART_CACHE_DIR, analysis_id)
        if os.path.exists(path):
            shutil.rmtree(path)
        path_full = os.path.join(path, last_modified, 'analysisFull.xml')
        path_short = os.path.join(path, last_modified, 'analysisShort.xml')
        save_to_cache(analysis_id, last_modified)
        self.assertTrue(os.path.exists(path_full))
        self.assertTrue(os.path.exists(path_short))
        shutil.rmtree(path)
        # check exception raises when file does not exists
        bad_analysis_id = 'bad-analysis-id'
        path = os.path.join(settings.CART_CACHE_DIR, bad_analysis_id)
        try:
            save_to_cache(bad_analysis_id, last_modified)
        except AnalysisFileException:
            pass
        else:
            raise False, 'AnalysisFileException doesn\'t raised'
        shutil.rmtree(path)
        # check case when file was updated
        path = os.path.join(settings.CART_CACHE_DIR, analysis_id)
        try:
            save_to_cache(analysis_id, '1900-10-29T21:56:12Z')
        except AnalysisFileException:
            pass
        else:
            raise False, 'AnalysisFileException doesn\'t raised'
        shutil.rmtree(path)


    def test_cache_generate_manifest_live(self):
        """
        Test if manifest collects only data from files where state='live'
        """
        response = self.client.post(reverse('cart_download_files', args=['manifest']))
        manifest = response.content
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.IDS_IN_CART[0] in manifest)
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.IDS_IN_CART[1] in manifest)
        self.assertFalse(self.IDS_IN_CART[2] in manifest)

    def test_cache_generate_manifest_no_live(self):
        """
        Test if manifest is an empty template when only element with state = 'bad_data' in cart
        """
        # remove all 'live' elements from cart
        url = reverse('cart_add_remove_files', args=['remove'])
        self.client.post(url,
            {'selected_files': [self.IDS_IN_CART[0], self.IDS_IN_CART[1]]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post(reverse('cart_download_files', args=['manifest']))
        self.assertTrue('<downloadable_file_size units="GB">0</downloadable_file_size>' in response.content)

    def test_cache_generate_metadata(self):
        """
        Test generating metadata in xml
        metadata should contain all elements
        """
        response = self.client.post(reverse('cart_download_files', args=['metadata']))
        metadata = response.content
        for id in self.IDS_IN_CART:
            self.assertTrue('<analysis_id>%s</analysis_id>' % id in metadata)

    def test_cache_generate_summary_tsv(self):
        """
        Test generating metadata in TSV
        metadata should contain all elements
        """
        response = self.client.post(reverse('cart_download_files', args=['summary']))
        content = response.content
        for id in self.IDS_IN_CART:
            self.assertTrue(id in content)
        self.assertTrue(all(field.lower().replace(' ', '_') in content
                            for field, visibility in settings.TABLE_COLUMNS))
'''

class CartCacheTestCase(WithCacheTestCase):

    cache_files = [
            '1b14aa46247842d46ff72d3ed0bf1ab5.xml',
            '4d3fee9f8557fc0de585af248b598c44.xml',
            'e7ccfb9ea17db39b27ae2b1d03e015e8.xml',
            '39ee3de2a4c531b8a871dc218d940a03.xml']

    """
    Cached files will be used
    7b9cd36a-8cbb-4e25-9c08-d62099c15ba1 - 2012-10-29T21:56:12Z
    8cab937e-115f-4d0e-aa5f-9982768398c2 - 2013-03-04T00:22:02Z

    satate = 'Submitted'
    db1cc50d-6340-4ecd-a1db-4ec17797ae75 - 2013-03-29T19:52:35Z
    """
    analysis_id = '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1'
    last_modified = '2012-10-29T21:56:12Z'
    analysis_id2 = '8cab937e-115f-4d0e-aa5f-9982768398c2'
    last_modified2 = '2013-03-04T00:22:02Z'
    analysis_id_not_live = 'db1cc50d-6340-4ecd-a1db-4ec17797ae75'
    last_modified_not_live = '2013-03-29T19:52:35Z'

    # will be removed from cache after every test
    ids = (analysis_id, analysis_id2, analysis_id_not_live,)

    def test_get_cache_file_path(self):
        self.assertEqual(
                get_cart_cache_file_path(
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                        '2012-10-29T21:56:12Z'),
                os.path.join(
                        settings.CART_CACHE_DIR,
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/2012-10-29T21:56:12Z/analysisFull.xml'))
        self.assertEqual(
                get_cart_cache_file_path(
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1',
                        '2012-10-29T21:56:12Z',
                        short=True),
                os.path.join(
                        settings.CART_CACHE_DIR,
                        '7b9cd36a-8cbb-4e25-9c08-d62099c15ba1/2012-10-29T21:56:12Z/analysisShort.xml'))

    def test_save_to_cart_cache(self):
        path = os.path.join(settings.CART_CACHE_DIR, self.analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        path_full = get_cart_cache_file_path(self.analysis_id, self.last_modified)
        path_short = get_cart_cache_file_path(self.analysis_id, self.last_modified, short=True)
        result = save_to_cart_cache(self.analysis_id, self.last_modified)
        # check that Results object returns
        self.assertEqual(result.Result.analysis_id, self.analysis_id)
        self.assertTrue(os.path.exists(path_full))
        self.assertTrue(os.path.exists(path_short))
        shutil.rmtree(path)
        # check exception raises when file does not exists
        bad_analysis_id = 'bad-analysis-id'
        path = os.path.join(settings.CART_CACHE_DIR, bad_analysis_id)
        if os.path.isdir(path):
            shutil.rmtree(path)
        try:
            save_to_cart_cache(bad_analysis_id, self.last_modified)
        except AnalysisFileException as e:
            self.assertEqual(unicode(e), 'File for analysis_id=bad-analysis-id, '
                'which was last modified 2012-10-29T21:56:12Z not exists, '
                'may be it was updated')
        else:
            raise False, 'AnalysisFileException doesn\'t raised'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check case when file was updated
        path = os.path.join(settings.CART_CACHE_DIR, self.analysis_id)
        try:
            save_to_cart_cache(self.analysis_id, '1900-10-29T21:56:12Z')
        except AnalysisFileException:
            pass
        else:
            raise False, 'AnalysisFileException doesn\'t raised'
        if os.path.isdir(path):
            shutil.rmtree(path)
        # check access denied to files outside cache dir
        try:
            save_to_cart_cache(self.analysis_id, '../../same_outside_dir')
        except AnalysisFileException as e:
            self.assertEqual(unicode(e), 'Bad analysis_id or last_modified')
        else:
            raise False, 'AnalysisFileException doesn\'t raised'

    def test_get_analysis(self):
        # test get_analysis_path
        path = os.path.join(settings.CART_CACHE_DIR, self.analysis_id)
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
        analysis = get_analysis(self.analysis_id, self.last_modified)
        self.assertEqual(analysis.Hits, 1)
        # short version
        analysis = get_analysis(self.analysis_id, self.last_modified, short=True)
        self.assertEqual(analysis.Hits, 1)
        # without cache
        shutil.rmtree(path)
        analysis = get_analysis(self.analysis_id, self.last_modified)
        self.assertEqual(analysis.Hits, 1)

    def test_join_analysises(self):
        data = (
                (self.analysis_id, self.last_modified),
                (self.analysis_id2, self.last_modified2))
        result = join_analysises(data)
        content = result.tostring()
        self.assertTrue(self.analysis_id in content)
        self.assertTrue(self.analysis_id2 in content)
        # check live only
        data = (
                (self.analysis_id, self.last_modified),
                (self.analysis_id_not_live, self.last_modified_not_live))
        result = join_analysises(data)
        content = result.tostring()
        self.assertTrue(self.analysis_id in content)
        self.assertTrue(self.analysis_id_not_live in content)
        result = join_analysises(data, live_only=True)
        content = result.tostring()
        self.assertTrue(self.analysis_id in content)
        self.assertFalse(self.analysis_id_not_live in content)

    def tearDown(self):
        super(CartCacheTestCase, self).tearDown()
        for i in self.ids:
            path = os.path.join(settings.CART_CACHE_DIR, i)
            if os.path.isdir(path):
                shutil.rmtree(path)


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
            'attributes': json.dumps(['size', 'center']),
            'filters': json.dumps({'center': '(1,2)', 'state': '(live)'}),
            'is_valid': True,
        }, {
            'filters': json.dumps({'center': '(1,2)', 'state': '(live)'}),
            'is_valid': False,
        }, {
            'attributes': 'bad_attributes',
            'filters': json.dumps({'center': '(1,2)', 'state': '(live)'}),
            'is_valid': False,
        }, {
            'attributes': json.dumps(['size', 'center']),
            'filters': json.dumps(['bad', 'filters']),
            'is_valid': False,
        }]

        for data in test_data_set:
            form = AllFilesForm(data)
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = AllFilesForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['attributes'],
            ['size', 'center'])
        self.assertEqual(
            form.cleaned_data['filters'],
            {'center': '(1,2)', 'state': '(live)'})
