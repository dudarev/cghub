"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test.testcases import TestCase

class CoreTests(TestCase):
    def test_index(self):
        """
        Tests that index page exists.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_non_existen_search(self):
        response = self.client.get('/search/?q=non_existent_search_query')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No results found' in response.content)

    def test_existent_search(self):
        response = self.client.get('/search/?q=6d7*')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Found' in response.content)
