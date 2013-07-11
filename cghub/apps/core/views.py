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

from cghub.apps.cart.utils import metadata
from cghub.apps.cart.cache import is_cart_cache_exists
from cghub.apps.cart.tasks import cache_file

from cghub.apps.core.attributes import ATTRIBUTES

from .utils import (
                get_filters_string, get_default_query, get_wsapi_settings,
                paginator_params, is_celery_alive, WSAPIRequest)
from .forms import BatchSearchForm


DEFAULT_QUERY = get_default_query()
DEFAULT_SORT_BY = None
WSAPI_SETTINGS = get_wsapi_settings()
core_logger = logging.getLogger('core')


def query_from_get(data):
    q = data.get('q')
    filter_str = get_filters_string(data)
    if q:
        # FIXME: temporary hack to work around GNOS not quoting Solr query
        if browser_text_search.useAllMetadataIndex:
            return u"all_metadata={0}".format(browser_text_search.ws_query(q)) + filter_str
        else:
            return u"xml_text={0}".format(u"("+q+u")") + filter_str
    return filter_str[1:]  # remove front ampersand


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
        result = WSAPIRequest(
                            query=self.query, sort_by=DEFAULT_SORT_BY,
                            limit=limit, settings=WSAPI_SETTINGS)
        context['num_results'] = result.hits
        context['results'] = result.results
        if result.hits == 0:
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
                queries_list = [query, u"analysis_id={0}".format(q)]
                # FIXME: need to handle queries_list properly
                result = WSAPIRequest(
                        query=queries_list[0], sort_by=sort_by,
                        offset=offset, limit=limit, settings=WSAPI_SETTINGS)
            else:
                result = WSAPIRequest(
                            query=query, sort_by=sort_by, offset=offset,
                            limit=limit, settings=WSAPI_SETTINGS)
            context['num_results'] = result.hits
            context['results'] = result.results
            if result.hits != 0:
                break

        if context['num_results'] == 0:
            context['message'] = 'No results found.'

        return context

    def dispatch(self, request, *args, **kwargs):
        # set default query if no query specified
        if not get_filters_string(request.GET) and not 'q' in request.GET:
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

    def post(self, request, **kwargs):
        form = BatchSearchForm(request.POST or None, request.FILES or None)
        found = {}
        unvalidated = []
        submitted = 0
        if form.is_valid():
            text = request.POST.get('text')
            submitted_ids = form.cleaned_data['ids']
            submitted_legacy_sample_ids = form.cleaned_data['legacy_sample_ids']
            # search by analysis_id and legacy_sample_id first
            # and then if some ids were not found,
            # search them by sample_id, participant_id and aliquot_id
            ids = []
            if submitted_ids:
                query = 'analysis_id=(%s)' % ' OR '.join(submitted_ids)
                result = WSAPIRequest(
                        query=query,
                        only_ids=True,
                        settings=WSAPI_SETTINGS)
                found['analysis_id'] = result.hits
                ids = result.results
                if result.hits != len(submitted_ids):
                    # search them by sample_id
                    query = 'sample_id=(%s)' % ' OR '.join(submitted_ids)
                    result = WSAPIRequest(
                            query=query,
                            only_ids=True,
                            settings=WSAPI_SETTINGS)
                    found['sample_id'] = result.hits
                    for id in result.results:
                        if id not in ids:
                            ids.append(id)
                    # search by participant_id and aliquot_id
                    query = 'participant_id=(%s)' % ' OR '.join(submitted_ids)
                    result = WSAPIRequest(
                            query=query,
                            only_ids=True,
                            settings=WSAPI_SETTINGS)
                    found['participant_id'] = result.hits
                    for id in result.results:
                        if id not in ids:
                            ids.append(id)
                    # search by aliquot_id
                    query = 'aliquot_id=(%s)' % ' OR '.join(submitted_ids)
                    result = WSAPIRequest(
                            query=query,
                            only_ids=True,
                            settings=WSAPI_SETTINGS)
                    found['aliquot_id'] = result.hits
                    for id in result.results:
                        if id not in ids:
                            ids.append(id)

            if submitted_legacy_sample_ids:
                query = 'legacy_sample_id=(%s)' % ' OR '.join(
                                            submitted_legacy_sample_ids)
                result = WSAPIRequest(
                        query=query,
                        only_ids=True,
                        settings=WSAPI_SETTINGS)
                found['legacy_sample_id'] = result.hits
                for id in result.results:
                    if id not in ids:
                        ids.append(id)

            # add files to cart
            if ids and 'add_to_cart' in request.GET:
                celery_alive = is_celery_alive()

                if 'cart' in request.session:
                    cart = request.session['cart']
                else:
                    cart = {}
                def callback(data):
                    analysis_id = data['analysis_id']
                    filtered_data = {}
                    for attr in ATTRIBUTES:
                        filtered_data[attr] = data.get(attr)
                    cart[analysis_id] = filtered_data
                    last_modified = data['last_modified']
                    if not is_cart_cache_exists(analysis_id, last_modified):
                        cache_file(analysis_id, last_modified, celery_alive)

                part = 0
                for part in range(0, len(ids), settings.MAX_ITEMS_IN_QUERY):
                    query = 'analysis_id=(%s)' % ' OR '.join(
                            ids[part : part + settings.MAX_ITEMS_IN_QUERY])
                    result = WSAPIRequest(
                        query=query, callback=callback, settings=WSAPI_SETTINGS)

                request.session['cart'] = cart

                return HttpResponseRedirect(reverse('cart_page'))

            unvalidated = form.cleaned_data.get('unvalidated_ids')
            submitted = (
                    len(form.cleaned_data.get('ids')) +
                    len(form.cleaned_data.get('legacy_sample_ids')) +
                    len(unvalidated))

            # show ids list in textarea even if they were submitted as file
            form = BatchSearchForm(initial={
                    'text': '\n'.join(form.cleaned_data['raw_ids'])})

        return self.render_to_response({
                    'form': form, 'found': found,
                    'submitted': submitted,
                    'unvalidated': unvalidated})


class ItemDetailsView(TemplateView):

    template_name = 'core/item_details.html'
    ajax_template_name = 'core/details_table.html'

    def get_context_data(self, **kwargs):
        result = WSAPIRequest(
                    query='analysis_id=%s' % kwargs['analysis_id'],
                    with_xml=True, full=True, settings=WSAPI_SETTINGS)
        if result.hits:
            xml = result.xml
            xml = xml[xml.find('<Result id="1">'): xml.find('</Result>') + 9]
            return {
                'res': result.results[0],
                'raw_xml': repr(xml.replace(' id="1"', '')),
                'analysis_id': kwargs['analysis_id']}
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
