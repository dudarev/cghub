import urllib

from django.views.generic.base import TemplateView

from cghub.cghub_api.api import request as api_request


class HomeView(TemplateView):
    template_name = 'core/home.html'


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        filter_str = ''
        allowed_attributes = [
                'center_name',
                'last_modified',
                'analyte_code',
                'sample_type',
                ]
        for attr in allowed_attributes:
            if self.request.GET.get(attr):
                filter_str += '&%s=%s' % (
                        attr, 
                        urllib.quote(self.request.GET.get(attr))
                        )
        if q:
            query = "xml_text=%s" % q
            query += filter_str
            print query
            results = api_request(query=query)
            if hasattr(results, 'Result'):
                context['num_results'] = len(results.Result)
                context['results'] = results.Result
            else:
                context['message'] = 'No results found.'
        return context
