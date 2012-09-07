"""
Test help pages
"""

from django.test import TestCase
from django.core.urlresolvers import reverse


class HelpTest(TestCase):
    def test_links_to_home(self):
        response = self.client.get(reverse('help_cart_page'))
        # two occurances in navigation bar /help/?from=/help/
        # one in text
        self.assertContains(response, '/help/', 3)
        response = self.client.get(reverse('help_search_page'))
        self.assertContains(response, '/help/', 3)
