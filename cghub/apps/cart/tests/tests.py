import os
import glob
import shutil
from lxml import etree, objectify

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from cghub.settings.utils import PROJECT_ROOT
from cghub.apps.cart.utils import cache_results


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
        self.failUnlessEqual('Cart (3)' in response.content, True)
        self.failUnlessEqual('Files in your cart: 3' in response.content, True)
        self.failUnlessEqual('3.00 Mb' in response.content, True)

        # make sure we have 3 files in cart
        self.failUnlessEqual(len(response.context['results']), 3)

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
        self.failUnlessEqual(len(response.context['results']), 1)

        # make sure counter in header is OK
        self.failUnlessEqual('Cart (1)' in response.content, True)
        self.failUnlessEqual('Files in your cart: 1' in response.content, True)

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
        self.failUnlessEqual(len(response.context['results']), 1)

        # make sure counter in header is OK
        self.failUnlessEqual('Cart (1)' in response.content, True)
        self.failUnlessEqual('Files in your cart: 1' in response.content, True)

        # make sure we do not have removed files in cart
        for f in rm_selected_files:
            self.assertEqual(f in response.content, False)


class CacheTestCase(TestCase):
    def test_cache_generate_manifest(self):
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
        manifest = None
        results_counter = 1
        for analysis_id in self.client.session.get('cart'):
            filename = "{0}_without_attributes".format(analysis_id)
            with open(os.path.join(api_results_cache_dir, filename)) as f:
                result = objectify.fromstring(f.read())
            if manifest is None:
                manifest = result
                manifest.Query.clear()
                manifest.Hits.clear()
            else:
                result.Result.set('id', u'{0}'.format(results_counter))
                manifest.insert(results_counter + 1, result.Result)
            results_counter += 1
        response = self.client.post(reverse('cart_download_files', args=['manifest']))
        content_manifest = etree.fromstring(response.content)
        self.assertEqual(set(manifest.getroottree().getroot().itertext()),
            set(content_manifest.getroottree().getroot().itertext()))
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
        settings.BROKER_URL = ''
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