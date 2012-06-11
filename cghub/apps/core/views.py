from django.views.generic.base import TemplateView
from cghub_api.api import request as api_request


class HomeView(TemplateView):
    template_name = 'core/home.html'


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q= self.request.GET.get('q')
        if q:
            results = api_request(query="xml_text=%s" % q)
            len(results)
            context['num_results'] = len(results.Result)
            context['results'] = results.Result
        return context
