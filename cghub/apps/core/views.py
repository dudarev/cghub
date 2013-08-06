import sys
import logging

from djcelery.models import TaskState
from celery import states
from urllib2 import URLError

from django.conf import settings
from django.http import (
                        QueryDict, HttpResponseRedirect, HttpResponse,
                        Http404, HttpResponseServerError)
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, View
from django.template import loader, Context

from cghub.wsapi import browser_text_search

from cghub.apps.cart.utils import metadata, load_missing_attributes
from cghub.apps.cart.cache import is_cart_cache_exists
from cghub.apps.cart.tasks import cache_file

from cghub.apps.core.attributes import ATTRIBUTES

from .utils import (
                get_filters_dict, get_default_query,
                paginator_params, is_celery_alive, RequestDetail,
                RequestIDs, RequestFull)
from .forms import BatchSearchForm, AnalysisIDsForm


DEFAULT_QUERY = get_default_query()
DEFAULT_SORT_BY = None
core_logger = logging.getLogger('core')


def query_from_get(data):
    q = data.get('q')
    filters = get_filters_dict(data)
    if q:
        # FIXME: temporary hack to work around GNOS not quoting Solr query
        if browser_text_search.useAllMetadataIndex:
            return {'all_metadata': browser_text_search.ws_query(q) + filter_str}
        else:
            filters.update({'xml_text': '(%s)' % q})
            return filters
    return filters


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
            get = {}
            for i in request.COOKIES[settings.LAST_QUERY_COOKIE].split('&'):
                parts = i.split('=')
                if len(parts) == 2 and parts[0] != 'q':
                    get[parts[0]] = parts[1]
            self.query = query_from_get(get)
        else:
            self.query = DEFAULT_QUERY
        # populating GET with query for proper work of applied_filters templatetag
        request.GET = QueryDict(self.query, mutable=True)
        return super(HomeView, self).get(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', DEFAULT_SORT_BY)
        offset, limit = paginator_params(self.request)
        # will be saved to cookie in get method
        self.paginator_limit = limit
        query = query_from_get(self.request.GET)

        # set offset to zero if no results returned
        for offset in (offset, 0):
            if 'xml_text' in query:
                # FIXME: this is temporary hack, need for multiple requests will fixed CGHub
                queries_list = [query, {'analysis_id': q}]
                # FIXME: need to handle queries_list properly
                api_request = RequestDetail(
                        query=queries_list[0], sort_by=sort_by,
                        offset=offset, limit=limit)
            else:
                api_request = RequestDetail(
                        query=query, sort_by=sort_by, offset=offset,
                        limit=limit)
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

    def dispatch(self, request, *args, **kwargs):
        # set default query if no query specified
        if not get_filters_dict(request.GET) and not 'q' in request.GET:
            return HttpResponseRedirect(reverse('search_page') + '?' + DEFAULT_QUERY)
        return super(SearchView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        # save current query to cookie
        if request.GET and response.status_code == 200:
            response.set_cookie(settings.LAST_QUERY_COOKIE,
                    request.GET.urlencode(safe='()[]*'),
                    max_age=settings.COOKIE_MAX_AGE,
                    path=reverse('home_page'))
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

    def search(self, submitted_ids, submitted_legacy_sample_ids):
        """
        Search by analysis_id and legacy_sample_id first.
        Then if some ids were not found,
        search them by sample_id, participant_id and aliquot_id.
        """
        found = {}
        ids = []
        if submitted_ids:
            query = {'analysis_id': submitted_ids}
            api_request = RequestIDs(query=query)
            ids = []
            for result in api_request.call():
                ids.append(result.analysis_id.text)
            found['analysis_id'] = api_request.hits
            if api_request.hits != len(submitted_ids):
                # search them by sample_id
                query = {'sample_id': submitted_ids}
                api_request = RequestIDs(query=query)
                for result in api_request.call():
                    analysis_id = result.analysis_id.text
                    if analysis_id not in ids:
                        ids.append(analysis_id)
                found['sample_id'] = api_request.hits
                # search by participant_id and aliquot_id
                query = {'participant_id':  submitted_ids}
                api_request = RequestIDs(query=query)
                for result in api_request.call():
                    analysis_id = result.analysis_id.text
                    if analysis_id not in ids:
                        ids.append(analysis_id)
                found['participant_id'] = api_request.hits
                # search by aliquot_id
                query = {'aliquot_id': submitted_ids}
                api_request = RequestIDs(query=query)
                for result in api_request.call():
                    analysis_id = result.analysis_id.text
                    if analysis_id not in ids:
                        ids.append(analysis_id)
                found['aliquot_id'] = api_request.hits

        if submitted_legacy_sample_ids:
            query = {'legacy_sample_id': submitted_legacy_sample_ids}
            api_request = RequestIDs(query=query)
            for result in api_request.call():
                analysis_id = result.analysis_id.text
                if analysis_id not in ids:
                    ids.append(analysis_id)
            found['legacy_sample_id'] = api_request.hits

        return ids, found

    def post(self, request, **kwargs):
        if 'ids' in request.POST:
            form = AnalysisIDsForm(request.POST)
            if form.is_valid():
                ids = form.cleaned_data['ids']
            else:
                return HttpResponseRedirect(reverse('batch_search_page'))

            if request.POST.get('add_to_cart'):
                celery_alive = is_celery_alive()

                if 'cart' in request.session:
                    cart = request.session['cart']
                else:
                    cart = {}

                part = 0
                for part in range(0, len(ids), settings.MAX_ITEMS_IN_QUERY):
                    query = {'analysis_id': ids[part : part + settings.MAX_ITEMS_IN_QUERY]}
                    api_request = RequestDetail(query=query)
                    for result in api_request.call():
                        analysis_id = result.analysis_id
                        filtered_data = {}
                        for attr in ATTRIBUTES:
                            filtered_data[attr] = result[attr]
                        cart[analysis_id] = filtered_data
                        last_modified = result.last_modified
                        if not is_cart_cache_exists(analysis_id, last_modified):
                            cache_file(analysis_id, last_modified, celery_alive)

                request.session['cart'] = cart

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
                    results.append({'analysis_id': i})
                results = load_missing_attributes(results)

                return self.render_to_response({
                        'form': form, 'ids': ids,
                        'results': results})
        else:
            # submitted search form
            form = BatchSearchForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                submitted_ids = form.cleaned_data['ids']
                submitted_legacy_sample_ids = form.cleaned_data['legacy_sample_ids']
                unvalidated = form.cleaned_data.get('unvalidated_ids')
                submitted = (
                        len(form.cleaned_data.get('ids')) +
                        len(form.cleaned_data.get('legacy_sample_ids')) +
                        len(unvalidated))

                ids, found = self.search(submitted_ids, submitted_legacy_sample_ids)

                ids = sorted(ids)
                results = []
                for i in ids[:settings.DEFAULT_PAGINATOR_LIMIT]:
                    results.append({'analysis_id': i})
                results = load_missing_attributes(results)

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
        try:
            result = api_request.call()[0]
            xml = result.xml
            xml = xml[xml.find('<Result id="1">'): xml.find('</Result>') + 9]
            return {
                'res': result,
                'raw_xml': repr(xml.replace(' id="1"', '')),
                'analysis_id': kwargs['analysis_id']}
        except IndexError:
            pass
        return {'res': None}

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
        return metadata(data={analysis_id: {
                'last_modified': request.GET.get('last_modified'),
                'state': request.GET.get('state')}})


class CeleryTasksView(TemplateView):
    template_name = 'core/celery_task_status.html'

    def get_context_data(self):
        from djcelery.humanize import naturaldate
        from djcelery.admin import TASK_STATE_COLORS
        # Showing last 50 task states
        tasks = TaskState.objects.all()[:50].values('task_id', 'state', 'name', 'tstamp')

        def prettify_task(task):
            task['tstamp'] = naturaldate(task['tstamp'])
            color = TASK_STATE_COLORS.get(task['state'], "black")
            task['state'] = "<b><span style=\"color: %s;\">%s</span></b>" % (color, task['state'])
            return task

        return {"tasks": map(prettify_task, tasks)}


class CeleryTaskStatusView(AjaxView):

    def get_context_data(self, task_id):
        try:
            task = TaskState.objects.get(task_id=task_id)
            if task.state == states.FAILURE:
                return {'status': 'failure'}
            if task.state == states.SUCCESS:
                return {'status': 'success'}
            return {'status': 'pending'}
        except TaskState.DoesNotExist:
            pass
        return {'status': 'failure'}

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        key = request.GET.get('task_id')
        context = self.get_context_data(key)
        return self.render_to_response(context)


def error_500(request):
    """
    Custom error 500 handler.
    Connected in cghub.urls.
    """
    t = loader.get_template('500.html')
    exc_type, value, tb = sys.exc_info()
    return HttpResponseServerError(
                t.render(Context({'wsapi_connection_error': exc_type == URLError})))
