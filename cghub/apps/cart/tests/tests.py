import os
import glob
import shutil
from lxml import etree, objectify

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from cghub.settings.utils import PROJECT_ROOT
from cghub.apps.cart.utils import cache_results

from cghub.apps.core.tests import WithCacheTestCase


class CartTests(TestCase):

    aids = (
            '12345678-1234-1234-1234-123456789abc',
            '12345678-4321-1234-1234-123456789abc',
            '87654321-1234-1234-1234-123456789abc')

    def setUp(self):
        self.client = Client()
        self.cart_page_url = reverse('cart_page')

    def test_cart_add_files(self):
        url = reverse('cart_add_remove_files', args=['add'])
        selected_files = ['file1', 'file2', 'file3']
        response = self.client.post(url, {'selected_files': selected_files,
                        'attributes': '{"file1":{"analysis_id":"%s", "files_size": 1048576},'
                        '"file2":{"analysis_id":"%s", "files_size": 1048576},'
                        '"file3":{"analysis_id":"%s", "files_size": 1048576}}' % self.aids
        })
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
        response = self.client.post(url, {'selected_files': selected_files,
                                          'attributes': '{"file1":{"analysis_id":"%s"}, '
                                                        '"file1":{"analysis_id":"%s"}, '
                                                        '"file1":{"analysis_id":"%s"}}' % self.aids
        })
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
        response = self.client.post(url, {'selected_files': selected_files,
                                          'attributes': '{"file1":{"analysis_id":"%s"},'
                                                        '"file2":{"analysis_id":"%s"},'
                                                        '"file3":{"analysis_id":"%s"}}' % self.aids
        })
        # remove files
        rm_selected_files = [self.aids[0], self.aids[1]]
        url = reverse('cart_add_remove_files', args=['remove'])
        response = self.client.post(url, {'selected_files': rm_selected_files})

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
                    **{'HTTP_REFERER':'http://somepage.com/%s' % params})
        self.assertRedirects(response, reverse('cart_page') + params)

    def test_cart_pagination(self):
        # add 3 files to cart
        url = reverse('cart_add_remove_files', args=['add'])
        selected_files = ['file1', 'file2', 'file3']
        response = self.client.post(url, {'selected_files': selected_files,
                                      'attributes': '{"file1":{"analysis_id":"%s", "files_size": 1048576},'
                                                    '"file2":{"analysis_id":"%s", "files_size": 1048576},'
                                                    '"file3":{"analysis_id":"%s", "files_size": 1048576}}' % self.aids
        })
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


class CartAddItemsTests(WithCacheTestCase):

    cache_files = [
        '32aca6fc099abe3ce91e88422edc0a20.xml'
    ]

    def test_add_all_items(self):
        attributes = ['study', 'center_name', 'analyte_code']
        filters = {
                'state': '(live)',
                'last_modified': '[NOW-1DAY TO NOW]',
                'analyte_code': '(D)'
                }
        url = reverse('cart_add_remove_files', args=['add'])
        response = self.client.post(
                    url,
                    {'attributes': json.dumps(attributes),
                    'filters': json.dumps(filters)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data, 'redirect')
        # check resultes was added to cart
        response = self.client.get(reverse('cart_page'))
        self.assertContains(response, 'Cart (14)')


class CacheTestCase(TestCase):
    def test_cache_generate_manifest(self):
        """
        Test if manifest collects only data from files where state='live'
        """
        testdata_dir = os.path.join(PROJECT_ROOT, 'test_data/test_cache')
        api_results_cache_dir = settings.CART_CACHE_FOLDER
        files = glob.glob(os.path.join(api_results_cache_dir, '*'))
        for file in files:
            os.remove(file)
        files = glob.glob(os.path.join(testdata_dir, '*'))
        for file in files:
            shutil.copy(file, os.path.join(api_results_cache_dir, os.path.basename(file)))
        url = reverse('cart_add_remove_files', args=['add'])
        self.client.post(url,
                {'selected_files': ['file1', 'file2', 'file3'],
                 'attributes': '{"file1":{"analysis_id":"4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6", "state": "live"},'
                               '"file2":{"analysis_id":"4b2235d6-ffe9-4664-9170-d9d2013b395f", "state": "live"},'
                               '"file3":{"analysis_id":"7be92e1e-33b6-4d15-a868-59d5a513fca1", "state": "bad_data"}}'
            })
        response = self.client.post(reverse('cart_download_files', args=['manifest']))
        manifest = etree.fromstring(response.content)
        self.assertTrue("4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6" in set(manifest.getroottree().getroot().itertext()))
        self.assertTrue("4b2235d6-ffe9-4664-9170-d9d2013b395f" in set(manifest.getroottree().getroot().itertext()))
        self.assertFalse("7be92e1e-33b6-4d15-a868-59d5a513fca1" in set(manifest.getroottree().getroot().itertext()))

        # leave only elements with state = 'bad_data'
        url = reverse('cart_add_remove_files', args=['remove'])
        self.client.post(url, {
            'selected_files': ['4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6',
                               '4b2235d6-ffe9-4664-9170-d9d2013b395f']})
        response = self.client.post(reverse('cart_download_files', args=['manifest']))
        self.assertContains(response, '<downloadable_file_count>0</downloadable_file_count>')

        files = glob.glob(os.path.join(api_results_cache_dir, '*'))
        for file in files:
            os.remove(file)

    def test_cache_generate_xml(self):
        testdata_dir = os.path.join(PROJECT_ROOT, 'test_data/test_cache')
        api_results_cache_dir = settings.CART_CACHE_FOLDER
        files = glob.glob(os.path.join(api_results_cache_dir, '*'))
        for file in files:
            os.remove(file)
        files = glob.glob(os.path.join(testdata_dir, '*'))
        for file in files:
            shutil.copy(file, os.path.join(api_results_cache_dir, os.path.basename(file)))
        selected_files = ['file1', 'file2', 'file3']
        self.client.post(reverse('cart_add_remove_files', args=['add']),
                {'selected_files': selected_files,
                 'attributes': '{"file1":{"analysis_id":"4b7c5c51-36d4-45a4-ae4d-0e8154e4f0c6"},'
                               '"file2":{"analysis_id":"4b2235d6-ffe9-4664-9170-d9d2013b395f"},'
                               '"file3":{"analysis_id":"7be92e1e-33b6-4d15-a868-59d5a513fca1"}}'
            })
        xml = None
        results_counter = 1
        for analysis_id in self.client.session.get('cart'):
            filename = "{0}_with_attributes".format(analysis_id)
            with open(os.path.join(api_results_cache_dir, filename)) as f:
                result = objectify.fromstring(f.read())
            if xml is None:
                xml = result
                xml.Query.clear()
                xml.Hits.clear()
            else:
                result.Result.set('id', u'{0}'.format(results_counter))
                xml.insert(results_counter + 1, result.Result)
            results_counter += 1
        response = self.client.post(reverse('cart_download_files', args=['xml']))
        content_xml = etree.fromstring(response.content)
        self.assertEqual(set(xml.getroottree().getroot().itertext()),
            set(content_xml.getroottree().getroot().itertext()))
        files = glob.glob(os.path.join(api_results_cache_dir, '*'))
        for file in files:
            os.remove(file)

    def test_cache_errors(self):
        """Testing caching cart is working when message broker is not running"""
        broker_url = settings.BROKER_URL
        settings.BROKER_URL = 'non_existent_url'
        settings.ADMINS = (('admin', 'admin@admin.com'),)
        try:
            cache_results({})
        except AttributeError:
            #   File "lxml.objectify.pyx", line 226, in lxml.objectify.ObjectifiedElement.__getattr__ (src/lxml/lxml.objectify.c:2894)
            #   File "lxml.objectify.pyx", line 485, in lxml.objectify._lookupChildOrRaise (src/lxml/lxml.objectify.c:5428)
            # AttributeError: no such child: Result
            pass
        import time
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            settings.EMAIL_SUBJECT_PREFIX + '[ucsc-cghub] ERROR: Message broker not working'
        )

        settings.BROKER_URL = broker_url
        settings.ADMINS = ()
