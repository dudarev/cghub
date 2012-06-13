from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart_page_url = reverse('cart_page')

    def test_cart_add_files(self):
        url = reverse('cart_add_remove_files', args=['add'])
        selected_files = ['file1', 'file2', 'file3']
        response = self.client.post(url, {'selected_files': selected_files,
            'attributes': '{"file1":{"legacy_sample_id":"file1", "filesize": 1048576},"file2":{"legacy_sample_id":"file2", "filesize": 1048576},"file3":{"legacy_sample_id":"file3", "filesize": 1048576}}'
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
        for f in selected_files:
            self.assertEqual(f in response.content, True)


    def test_card_add_duplicate_files(self):
        url = reverse('cart_add_remove_files', args=['add'])
        selected_files = ['file1', 'file1', 'file1']
        response = self.client.post(url, {'selected_files': selected_files,
            'attributes': '{"file1":{"legacy_sample_id":"file1"},"file1":{"legacy_sample_id":"file1"},"file1":{"legacy_sample_id":"file1"}}'
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
            'attributes': '{"file1":{"legacy_sample_id":"file1"},"file2":{"legacy_sample_id":"file2"},"file3":{"legacy_sample_id":"file3"}}'
        })

        # remove files
        rm_selected_files = ['file1', 'file3']
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