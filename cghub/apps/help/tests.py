from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from cghub.apps.help.urls import urlpatterns
from cghub.apps.help.models import HelpText


class HelpViewsTestCase(TestCase):

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
        self.assertContains(response, '/help/', 5)
        response = self.client.get(reverse('help_search_page'))
        self.assertContains(response, '/help/', 5)

    def test_help_hint_text(self):
        """
        ajax view for obtaining help hints text
        """
        ajax_attrs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        help_hint_key = 'UUID'
        help_hint_text = 'Some hint text'
        with self.settings(HELP_HINTS = {help_hint_key: help_hint_text}):
            url = reverse('help_hint')
            # test not ajax
            r = self.client.get(url)
            self.assertEqual(r.status_code, 404)
            r = self.client.get(url, {}, **ajax_attrs)
            self.assertFalse(json.loads(r.content)['success'])
            r = self.client.get(url, {'key': 'badkey'}, **ajax_attrs)
            self.assertFalse(json.loads(r.content)['success'])
            r = self.client.get(url, {'key': help_hint_key}, **ajax_attrs)
            data = json.loads(r.content)
            self.assertTrue(data['success'])
            self.assertEqual(data['text'], help_hint_text)

    def test_help_text(self):
        """
        Should return title and content for specified slug
        """
        ajax_attrs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        test_data = {
            'slug': 'some-slug',
            'title': 'Some title',
            'content': 'Some content'
        }
        # try not ajax
        r = self.client.get(reverse('help_text'), {'slug': test_data['slug']})
        self.assertEqual(r.status_code, 404)
        # try to get not existing text
        r = self.client.get(
                        reverse('help_text'),
                        {'slug': test_data['slug']},
                        **ajax_attrs)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data, {'success': False})
        # create record and try again
        HelpText.objects.create(**test_data)
        r = self.client.get(
                        reverse('help_text'),
                        {'slug': test_data['slug']},
                        **ajax_attrs)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['title'], test_data['title'])
        self.assertEqual(data['content'], test_data['content'])


class HelpModelsTestCase(TestCase):

    def test_help_text_unicode(self):
        test_data = {
            'slug': 'some-slug',
            'title': 'Some title',
            'content': 'Some content'
        }
        help_text = HelpText(**test_data)
        self.assertEqual(unicode(help_text), test_data['title'])
