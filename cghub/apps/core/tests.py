from django.test.testcases import TestCase
from django.template import Template, Context
from django.http import HttpRequest


class CoreTests(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_non_existent_search(self):
        response = self.client.get('/search/?q=non_existent_search_query')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No results found' in response.content)

    def test_existent_search(self):
        response = self.client.get('/search/?q=6d7*')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Found' in response.content)


class TestTemplateTags(TestCase):
    def test_sort_link_tag(self):
        test_request = HttpRequest()
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
            ).render(Context({
                    'request': test_request
                }))
                
        self.assertEqual(out, 
            '<a href="?sort_by=last_modified">Date Uploaded</a>')
            
        # make sure that other request.GET variables are preserved
        test_request.GET.update({'q': 'sample_query'})
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
            ).render(Context({
                    'request': test_request
                }))
                
        self.assertEqual(out, 
            '<a href="?q=sample_query&sort_by=last_modified">Date Uploaded</a>')
            
        # make sure that direction label is rendered if it is active sort filter
        del(test_request.GET['q'])
        test_request.GET.update({'sort_by': 'last_modified'})
        out = Template(
            "{% load search_tags %}"
            "{% sort_link request 'last_modified' 'Date Uploaded' %}"
            ).render(Context({
                    'request': test_request
                }))
                
        self.assertEqual(out, 
            '<a href="?sort_by=-last_modified">Date Uploaded DESC</a>')
