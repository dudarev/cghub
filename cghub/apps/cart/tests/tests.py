import os
import glob
import shutil
import datetime

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.contrib.sessions.models import Session

from cghub.settings.utils import PROJECT_ROOT
from cghub.apps.cart.utils import cache_results
from cghub.apps.cart.tasks import add_files_to_cart_by_query
from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm

from cghub.apps.core.tests import WithCacheTestCase


class CartTests(TestCase):

    aids = ('12345678-1234-1234-1234-123456789abc',
            '12345678-4321-1234-1234-123456789abc',
            '87654321-1234-1234-1234-123456789abc')

    def setUp(self):
        self.client = Client()
        self.cart_page_url = reverse('cart_page')

    def test_cart_add_files(self):
        url = reverse('cart_add_remove_files', args=['add'])
        selected_files = ['file1', 'file2', 'file3']
        response = self.client.post(
                        url,
                        {'selected_files': selected_files,
                         'attributes': '{"file1":{"analysis_id":"%s", "files_size": 1048576},'
                                        '"file2":{"analysis_id":"%s", "files_size": 1048576},'
                                        '"file3":{"analysis_id":"%s", "files_size": 1048576}}' % self.aids},
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
        for f in self.aids:
            self.assertEqual(f in response.content, True)

    def test_card_add_duplicate_files(self):
        url = reverse('cart_add_remove_files', args=['add'])
        selected_files = ['file1', 'file1', 'file1']
        response = self.client.post(
                        url,
                        {'selected_files': selected_files,
                            'attributes': '{"file1":{"analysis_id":"%s"}, '
                            '"file1":{"analysis_id":"%s"}, '
                            '"file1":{"analysis_id":"%s"}}' % self.aids},
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
        selected_files = ['file1', 'file2', 'file3']
        response = self.client.post(
                            url, 
                            {'selected_files': selected_files,
                                    'attributes': '{"file1":{"analysis_id":"%s"},'
                                    '"file2":{"analysis_id":"%s"},'
                                    '"file3":{"analysis_id":"%s"}}' % self.aids},
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # remove files
        rm_selected_files = [self.aids[0], self.aids[1]]
        url = reverse('cart_add_remove_files', args=['remove'])
        response = self.client.post(
                        url,
                        {'selected_files': rm_selected_files},
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
        rm_selected_files = [self.aids[2]]
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
        selected_files = ['file1', 'file2', 'file3']
        response = self.client.post(
                                url,
                                {'selected_files': selected_files,
                                 'attributes': '{"file1":{"analysis_id":"%s", "files_size": 1048576},'
                                                '"file2":{"analysis_id":"%s", "files_size": 1048576},'
                                                '"file3":{"analysis_id":"%s", "files_size": 1048576}}' % self.aids},
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
        response = self.client.get(reverse(
                                'cart_add_remove_files',
                                args=['add']))
        self.assertEqual(response.status_code, 404)


class CartAddItemsTestCase(WithCacheTestCase):

    cache_files = [
        '32aca6fc099abe3ce91e88422edc0a20.xml'
    ]

    def test_add_files_to_cart_by_query(self):
        """
        Celery task.
        Used by cart_add_files.
        Obtains files for specified query and adds them to cart.
        """
        data = {
            'attributes': ['study', 'center_name', 'analyte_code'],
            'filters': {
                        'state': '(live)',
                        'last_modified': '[NOW-1DAY TO NOW]',
                        'analyte_code': '(D)'}}
        # check do nothing when session not exists
        session_key = 'some-bad-session-key'
        add_files_to_cart_by_query(data, session_key)
        self.assertFalse(Session.objects.filter(session_key=session_key).exists())
        # Create session and check one more time
        s = Session(
            expire_date=datetime.datetime.now() + datetime.timedelta(days=7))
        s.save()
        add_files_to_cart_by_query(data, s.session_key)
        session = Session.objects.get(session_key=s.session_key)
        cart = session.get_decoded()['cart']
        self.assertEqual(len(cart), 14)


class CacheTestCase(TestCase):
    IDS_IN_CART = ("4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6",
                   "4b2235d6-ffe9-4664-9170-d9d2013b395f",
                   "7be92e1e-33b6-4d15-a868-59d5a513fca1")
    def setUp(self):
        testdata_dir = os.path.join(PROJECT_ROOT, 'test_data/test_cache')
        self.api_results_cache_dir = settings.CART_CACHE_DIR
        files = glob.glob(os.path.join(self.api_results_cache_dir, '*'))
        for file in files:
            os.remove(file)
        files = glob.glob(os.path.join(testdata_dir, '*'))
        for file in files:
            shutil.copy(file, os.path.join(self.api_results_cache_dir, os.path.basename(file)))

        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url, {'selected_files': ['file1', 'file2', 'file3'],
                               'attributes': '{"file1":{"analysis_id":"%s", "state": "live"},'
                                              '"file2":{"analysis_id":"%s", "state": "live"},'
                                              '"file3":{"analysis_id":"%s", "state": "bad_data"}}' % self.IDS_IN_CART},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def tearDown(self):
        files = glob.glob(os.path.join(self.api_results_cache_dir, '*'))
        for file in files:
            os.remove(file)

    def test_cache_generate_manifest_xml_live(self):
        """
        Test if manifest collects only data from files where state='live'
        """
        response = self.client.post(reverse('cart_download_files', args=['manifest_xml']))
        manifest = response.content
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.IDS_IN_CART[0] in manifest)
        self.assertTrue('<analysis_id>%s</analysis_id>' % self.IDS_IN_CART[1] in manifest)
        self.assertFalse(self.IDS_IN_CART[2] in manifest)

    def test_cache_generate_manifest_xml_no_live(self):
        """
        Test if manifest is an empty template when only element with state = 'bad_data' in cart
        """
        # remove all 'live' elements from cart
        url = reverse('cart_add_remove_files', args=['remove'])
        self.client.post(url,
            {'selected_files': [self.IDS_IN_CART[0], self.IDS_IN_CART[1]]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post(reverse('cart_download_files', args=['manifest_xml']))
        self.assertTrue('<downloadable_file_size units="GB">0</downloadable_file_size>' in response.content)

    def test_cache_generate_manifest_tsv(self):
        """
        Test generating manifest in TSV
        metadata should contain only elements with state='live'
        """
        response = self.client.post(reverse('cart_download_files', args=['manifest_tsv']))
        content = response.content
        self.assertTrue(self.IDS_IN_CART[0] in content)
        self.assertTrue(self.IDS_IN_CART[1] in content)
        self.assertFalse(self.IDS_IN_CART[2] in content)
        self.assertTrue(all(tag in content for tag in ['id', 'analysis_id', 'state', 'analysis_data_uri']))

    def test_cache_generate_metadata_xml(self):
        """
        Test generating metadata in xml
        metadata should contain all elements
        """
        response = self.client.post(reverse('cart_download_files', args=['metadata_xml']))
        metadata = response.content
        for id in self.IDS_IN_CART:
            self.assertTrue('<analysis_id>%s</analysis_id>' % id in metadata)

    def test_cache_generate_metadata_tsv(self):
        """
        Test generating metadata in TSV
        metadata should contain all elements
        """
        response = self.client.post(reverse('cart_download_files', args=['metadata_tsv']))
        content = response.content
        for id in self.IDS_IN_CART:
            self.assertTrue(id in content)
        self.assertTrue(all(tag in content for tag in ['id', 'analysis_id', 'state', 'analysis_data_uri', 'aliquot_id', 'filename']))


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
            if not form.is_valid():
                print form.errors
            self.assertEqual(form.is_valid(), data['is_valid'])

        form = SelectedFilesForm(test_data_set[0])
        form.is_valid()
        self.assertEqual(
            form.cleaned_data['attributes']['7850f073-642a-40a8-b49d-e328f27cfd66'],
            {'study': 'TCGA', 'size': 10})
        self.assertEqual(
            form.cleaned_data['selected_files'][0],
            '7850f073-642a-40a8-b49d-e328f27cfd66')

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
