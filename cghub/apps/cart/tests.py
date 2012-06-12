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
        response = self.client.post(url, {'selected_files': selected_files})
        self.assertEqual(response.status_code, 302)
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)
        # make sure we have 3 files in cart
        self.failUnlessEqual(len(response.context['cart']), 3)
        # make sure we have files we've posted
        for f in selected_files:
            self.assertEqual(f in response.content, True)

    def test_card_add_duplicate_files(self):
        url = reverse('cart_add_remove_files', args=['add'])
        selected_files = ['file1', 'file1', 'file1']
        response = self.client.post(url, {'selected_files': selected_files})
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)
        # make sure we have only 1 file in cart
        self.failUnlessEqual(len(response.context['cart']), 1)

    def test_cart_remove_files(self):
        # add files
        url = reverse('cart_add_remove_files', args=['add'])
        add_selected_files = ['file1', 'file2', 'file3', 'file4']
        response = self.client.post(url, {'selected_files': add_selected_files})
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.assertEqual(response.status_code, 200)

        # remove files
        rm_selected_files = ['file2', 'file4']
        url = reverse('cart_add_remove_files', args=['remove'])
        response = self.client.post(url, {'selected_files': rm_selected_files})
        # go to cart page
        response = self.client.get(self.cart_page_url)
        self.failUnlessEqual(len(response.context['cart']), 2)
        # make sure we do not have removed files in cart
        for f in rm_selected_files:
            self.assertEqual(f in response.content, False)
