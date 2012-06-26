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
        sort_by = self.request.GET.get('sort_by', None)
        if sort_by:
            sort_by = urllib.quote(sort_by)
        filter_str = ''
        allowed_attributes = [
            'center_name',
            'last_modified',
            'analyte_code',
            'sample_type',
            'library_strategy',
            'disease_abbr',
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
            results = api_request(query=query, sort_by=sort_by)
            if hasattr(results, 'Result'):
                context['num_results'] = results.Hits
                context['results'] = results.Result
            else:
                context['num_results'] = 0
                context['message'] = 'No results found.'
        return context


class HelpView(TemplateView):
    template_name = 'core/help.html'
