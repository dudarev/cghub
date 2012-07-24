import urllib

from django.conf import settings
from django.http import QueryDict
from django.utils.http import urlquote

from django.views.generic.base import TemplateView
from cghub.cghub_api.api import request as api_request


class HomeView(TemplateView):
    template_name = 'core/search.html'
    default_query = 'last_modified=[NOW-7DAY%20TO%20NOW]'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        limit = settings.DEFAULT_PAGINATOR_LIMIT
        results = api_request(query=self.default_query, sort_by='-last_modified',
            limit=limit)
        results.calculate_files_size()
        if hasattr(results, 'Result'):
            context['num_results'] = int(results.Hits.text)
            context['results'] = results.Result
        else:
            context['num_results'] = 0
            context['message'] = 'No results found.'
        return context

    def get(self, request, *args, **kwargs):
        # populating GET with query for proper work of applied_filters templatetag
        request.GET = QueryDict(self.default_query, mutable=True)
        return super(HomeView, self).get(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')
        offset = self.request.GET.get('offset')
        offset = offset and offset.isdigit() and int(offset) or 0
        limit = self.request.GET.get('limit')
        limit = limit and limit.isdigit() and int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
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
        query = u''
        if q:
            query = u"xml_text={0}".format(urlquote(q))
        query += filter_str
        results = api_request(query=query, sort_by=sort_by, offset=offset, limit=limit)
        # this function calculates files_size attribute
        results.calculate_files_size()
        if hasattr(results, 'Result'):
            context['num_results'] = int(results.Hits.text)
            context['results'] = results.Result
        else:
            context['num_results'] = 0
            context['message'] = 'No results found.'
        return context


class HelpView(TemplateView):
    template_name = 'core/help.html'
