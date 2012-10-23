from django.test import TestCase
from django.core.urlresolvers import reverse

from cghub.apps.help.urls import urlpatterns


class HelpTest(TestCase):

    def test_help_views(self):
        for pattern in urlpatterns:
            if (
                    pattern.name and
                    pattern.name.startswith('help') and
                    pattern.name.endswith('page')):
                response = self.client.get(reverse(pattern.name))
                self.assertEqual(response.status_code, 200)

    def test_links_to_home(self):
        response = self.client.get(reverse('help_cart_page'))
        # two occurances in navigation bar /help/?from=/help/
        # one in text
        self.assertContains(response, '/help/', 3)
        response = self.client.get(reverse('help_search_page'))
        self.assertContains(response, '/help/', 3)
