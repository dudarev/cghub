import urllib

from django.conf import settings
from django.http import QueryDict, HttpResponseRedirect
from django.utils.http import urlquote
from django.core.urlresolvers import reverse


from django.views.generic.base import TemplateView
from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import multiple_request as api_multiple_request


class HomeView(TemplateView):
    template_name = 'core/search.html'
    default_query = 'last_modified=[NOW-1MONTH%20TO%20NOW]'

    def dispatch(self, request, *args, **kwargs):
        # if there are any GET parameters - redirect to search page
        if request.GET:
            return HttpResponseRedirect(reverse('search_page') + '?' + request.GET.urlencode())
        return super(HomeView, self).dispatch(request, *args, **kwargs)

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
            'study',
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
            query = u"xml_text={0}".format(urlquote(q))
            query += filter_str
        else:
            query = filter_str[1:]  # remove front ampersand

        if 'xml_text' in query:
            queries_list = [query, query.replace('xml_text', 'analysis_id', 1)]
            results = api_multiple_request(queries_list=queries_list, sort_by=sort_by,
                offset=offset, limit=limit)
        else:
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

    def dispatch(self, request, *args, **kwargs):
        # if there are no any `q` query parameters
        # and now `last_modified` is specified
        # redirect to search page with last 7 days results
        q = request.GET.get('q')
        last_modified = request.GET.get('last_modified')
        if not q and not last_modified:
            GET_parameters = request.GET.copy()
            GET_parameters['last_modified'] = '[NOW-1MONTH TO NOW]'
            return HttpResponseRedirect(reverse('search_page') + '?' + GET_parameters.urlencode())
        return super(SearchView, self).dispatch(request, *args, **kwargs)


class ItemDetailsView(TemplateView):
    template_name = 'core/item_details.html'

    def get_context_data(self, **kwargs):
        return {}
