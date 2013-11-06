import logging
import sys

from urllib2 import URLError

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.template import loader, Context, RequestContext
from django.utils import simplejson as json
from django.http import (
            QueryDict, HttpResponseRedirect, HttpResponse,
            HttpResponseServerError)
from django.views.generic.base import TemplateView, View

from cghub.apps.cart.utils import item_metadata, Cart

from cghub.apps.core import browser_text_search
from .attributes import ATTRIBUTES
from .forms import BatchSearchForm, AnalysisIDsForm
from .requests import (
            RequestDetail, RequestFull, RequestMinimal, SearchByIDs,
            get_results_for_ids)
from .utils import (
            get_filters_dict, query_dict_to_str, paginator_params,
            add_message)


DEFAULT_SORT_BY = None
core_logger = logging.getLogger('core')


class AjaxView(View):

    http_method_names = ['get']
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(json.dumps(context), **response_kwargs)


class HomeView(TemplateView):
    template_name = 'core/search.html'

    def dispatch(self, request, *args, **kwargs):
        # if there are any GET parameters - redirect to search page
        if request.GET:
            return HttpResponseRedirect(
                    reverse('search_page') + '?' + request.GET.urlencode())
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        offset, limit = paginator_params(self.request)
        api_request = RequestDetail(
                    query=self.query, sort_by=DEFAULT_SORT_BY, limit=limit)
        results = []
        for result in api_request.call():
            results.append(result)
        context['num_results'] = api_request.hits
        context['results'] = results
        if api_request.hits == 0:
            context['message'] = 'No results found.'
        return context

    def get(self, request, *args, **kwargs):
        if settings.LAST_QUERY_COOKIE in request.COOKIES:
            self.query = {}
            for i in request.COOKIES[settings.LAST_QUERY_COOKIE].split('&'):
                parts = i.split('=')
                if len(parts) == 2:
                    self.query[parts[0]] = parts[1]
            self.query = get_filters_dict(self.query)
        else:
            self.query = settings.DEFAULT_FILTERS
        # populating GET with query for proper work of applied_filters templatetag
        request.GET = QueryDict(query_dict_to_str(self.query), mutable=True)
        return super(HomeView, self).get(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        sort_by = self.request.GET.get('sort_by', DEFAULT_SORT_BY)
        offset, limit = paginator_params(self.request)
        # will be saved to cookie in get method
        self.paginator_limit = limit
        filters = get_filters_dict(self.request.GET)

        # set offset to zero if no results returned
        for offset in (offset, 0):
            if q:
                # search by ids first
                search = SearchByIDs(
                        ids=[q],
                        filters=filters,
                        request_cls=RequestDetail)
                if not search.is_empty():
                    results = search.get_results()
                    context['results'] = results[offset:offset + limit]
                    context['num_results'] = len(results)
                    return context
                else:
                    # FIXME: temporary hack to work around GNOS not quoting Solr query
                    if browser_text_search.useAllMetadataIndex:
                        filters.update({'all_metadata': browser_text_search.ws_query(q)})
                    else:
                        filters.update({'xml_text': '(%s)' % q})
                    context['search_notification'] = ('<strong>Warning:</strong> '
                            'these results were produced by a free text '
                            'work search of the metadata. The results maybe '
                            'be incomplete or inconsistent due to limited '
                            'about of textual data available. Use the '
                            'filters to get s consistent set of results or '
                            'search for a particular identifier.')

            api_request = RequestDetail(
                    query=filters, sort_by=sort_by, offset=offset, limit=limit)
            results = []
            for result in api_request.call():
                results.append(result)
            context['num_results'] = api_request.hits
            context['results'] = results
            if api_request.hits != 0:
                break

        if context['num_results'] == 0:
            context['message'] = 'No results found.'

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        # save current query to cookie
        if response.status_code == 200:
            if request.GET and request.GET.get('remember', 'false') == 'true':
                query = request.GET.urlencode(safe='()[]*')
                response.set_cookie(settings.LAST_QUERY_COOKIE,
                        query,
                        max_age=settings.COOKIE_MAX_AGE,
                        path=reverse('home_page'))
            else:
                response.delete_cookie(settings.LAST_QUERY_COOKIE)
            response.set_cookie(settings.PAGINATOR_LIMIT_COOKIE,
                    self.paginator_limit,
                    max_age=settings.COOKIE_MAX_AGE,
                    path=reverse('home_page'))
        return response


class BatchSearchView(TemplateView):
    template_name = 'core/batch_search.html'

    def get(self, request, *args, **kwargs):
        form = BatchSearchForm()
        return self.render_to_response({'form': form})

    def post(self, request, **kwargs):
        if 'ids' in request.POST:
            form = AnalysisIDsForm(request.POST)
            if form.is_valid():
                ids = form.cleaned_data['ids']
            else:
                return HttpResponseRedirect(reverse('batch_search_page'))

            if request.POST.get('add_to_cart'):

                cart = Cart(request.session)
                with transaction.commit_on_success():
                    for part in range(0, len(ids), settings.MAX_ITEMS_IN_QUERY):
                        query = {'analysis_id': ids[part : part + settings.MAX_ITEMS_IN_QUERY]}
                        api_request = RequestMinimal(query=query)
                        for result in api_request.call():
                            cart.add(result)
                    cart.update_stats()

                return HttpResponseRedirect(reverse('cart_page'))
            else:
                ids = sorted(ids)
                results = []
                try:
                    offset = int(request.GET.get('offset', 0))
                    limit = int(request.GET.get(
                            'limit', settings.DEFAULT_PAGINATOR_LIMIT))
                except ValueError:
                    offset = 0
                    limit = settings.DEFAULT_PAGINATOR_LIMIT
                for i in ids[offset:(offset + limit)]:
                    results.append(i)

                results = get_results_for_ids(results, sort_by='analysis_id')

                return self.render_to_response({
                        'form': form, 'ids': ids,
                        'results': results})
        else:
            # submitted search form
            form = BatchSearchForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                submitted_ids = form.cleaned_data['ids']
                unvalidated = form.cleaned_data.get('unvalidated_ids')
                submitted = len(submitted_ids) + len(unvalidated)

                ids = []
                found = {}
                for part in range(0, len(submitted_ids), settings.MAX_ITEMS_IN_QUERY):
                    ids_part = submitted_ids[part : part + settings.MAX_ITEMS_IN_QUERY]
                    search = SearchByIDs(ids=ids_part)
                    for attr in search.results:
                        l = len(search.results[attr])
                        if l:
                            found[attr] = found.get(attr, 0) + l
                    ids += search.get_ids()
                ids = sorted(ids)
                offset, limit = paginator_params(request)
                results = get_results_for_ids(
                        ids[offset:offset + limit],
                        sort_by='analysis_id')

                if not results:
                    form.errors['__all__'] = form.error_class(["No results found."])
                return self.render_to_response({
                        'form': form, 'found': found, 'ids': ids,
                        'submitted': submitted, 'results': results,
                        'unvalidated': unvalidated})
            return self.render_to_response({
                        'form': form, 'found': None})


class ItemDetailsView(TemplateView):

    template_name = 'core/item_details.html'
    ajax_template_name = 'core/details_table.html'

    def get_context_data(self, **kwargs):
        api_request = RequestFull(query={'analysis_id': kwargs['analysis_id']})
        is_ajax = self.request.GET.get('ajax')
        cart = Cart(self.request.session)
        try:
            result = api_request.call().next()
            xml = result['xml']
            xml = xml[xml.find('<Result id="1">'): xml.find('</Result>') + 9]
            xml = xml.replace(' id="1"', '')
            xml = repr(xml)
            if xml[0] == 'u':
                xml = xml[1:]
            return {
                'res': result,
                'raw_xml': xml,
                'is_ajax': is_ajax,
                'analysis_id': kwargs['analysis_id'],
                'in_cart': cart.in_cart(analysis_id=kwargs['analysis_id'])}
        except StopIteration:
            pass
        raise URLError('No results for analysis_id == %s' % kwargs['analysis_id'])

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]


class MetadataView(View):
    def get(self, request, analysis_id):
        return item_metadata(
                analysis_id=analysis_id,
                last_modified=request.GET.get('last_modified'))


class MessageView(AjaxView):

    http_method_names = ['post']

    def post(self, request, message_id):
        messages = request.session.get('messages')
        if not messages:
            return self.render_to_response({'success': False})
        message_id = int(message_id)
        if message_id in messages:
            del messages[message_id]
            request.session['messages'] = messages
            request.session.modified = True
        return self.render_to_response({'success': True})


def error_500(request):
    """
    Custom error 500 handler.
    Connected in cghub.urls.
    """
    t = loader.get_template('500.html')
    exc_type, value, tb = sys.exc_info()
    context = RequestContext(request)
    if exc_type == URLError:
        context['error'] = value
    else:
        context['error'] = None
    return HttpResponseServerError(t.render(Context(context)))
