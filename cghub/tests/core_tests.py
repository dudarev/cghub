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
