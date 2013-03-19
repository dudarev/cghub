import urllib

from djcelery.models import TaskState
from celery import states
from lxml import etree

from django.conf import settings
from django.http import QueryDict, HttpResponseRedirect, HttpResponse, Http404
from django.utils.http import urlquote
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, View

from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import multiple_request as api_multiple_request

from cghub.apps.core.utils import (get_filters_string, get_default_query,
                                            get_wsapi_settings, metadata)


DEFAULT_QUERY = get_default_query()
DEFAULT_SORT_BY = '-upload_date'
WSAPI_SETTINGS = get_wsapi_settings()


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
            return HttpResponseRedirect(reverse('search_page') + '?' + request.GET.urlencode())
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        limit = settings.DEFAULT_PAGINATOR_LIMIT
        results = api_request(query=DEFAULT_QUERY, sort_by=DEFAULT_SORT_BY,
                                limit=limit, use_api_light=True,
                                settings=WSAPI_SETTINGS)
        results.add_custom_fields()
        if hasattr(results, 'Result'):
            context['num_results'] = results.length or int(results.Hits.text)
            context['results'] = results.Result
        else:
            context['num_results'] = 0
            context['message'] = 'No results found.'
        return context

    def get(self, request, *args, **kwargs):
        # populating GET with query for proper work of applied_filters templatetag
        request.GET = QueryDict(DEFAULT_QUERY, mutable=True)
        return super(HomeView, self).get(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', DEFAULT_SORT_BY)
        offset = self.request.GET.get('offset')
        offset = offset and offset.isdigit() and int(offset) or 0
        limit = self.request.GET.get('limit')
        limit = limit and limit.isdigit() and int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
        if sort_by:
            sort_by = urllib.quote(sort_by)
        filter_str = get_filters_string(self.request.GET)

        if q:
            query = u"xml_text={0}".format(urlquote(q))
            query += filter_str
        else:
            query = filter_str[1:]  # remove front ampersand

        if 'xml_text' in query:
            queries_list = [query, query.replace('xml_text', 'analysis_id', 1)]
            results = api_multiple_request(
                queries_list=queries_list, sort_by=sort_by,
                offset=offset, limit=limit, settings=WSAPI_SETTINGS)
        else:
            results = api_request(query=query, sort_by=sort_by,
                        offset=offset, limit=limit, use_api_light=True,
                        settings=WSAPI_SETTINGS)

        # this function calculates files_size attribute
        # and adds refassem_short_name to Results
        results.add_custom_fields()

        if hasattr(results, 'Result'):
            context['num_results'] = results.length or int(results.Hits.text)
            context['results'] = results.Result
        else:
            context['num_results'] = 0
            context['message'] = 'No results found.'
        return context

    def dispatch(self, request, *args, **kwargs):
        # set default query if no query specified
        if not get_filters_string(request.GET) and not 'q' in request.GET:
            return HttpResponseRedirect(reverse('search_page') + '?' + DEFAULT_QUERY)
        return super(SearchView, self).dispatch(request, *args, **kwargs)

class ItemDetailsView(TemplateView):

    template_name = 'core/item_details.html'
    ajax_template_name = 'core/details_table.html'

    def get_context_data(self, **kwargs):
        results = api_request(query='analysis_id=%s' % kwargs['uuid'],
                                    settings=WSAPI_SETTINGS)
        results.add_custom_fields()
        if hasattr(results, 'Result'):
            return {
                'res': results.Result,
                'raw_xml': repr(etree.tostring(results.Result).replace(' id="1"', '')),
                'uuid': kwargs['uuid']}
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
    def post(self, request, uuid):
        return metadata(ids=[uuid])


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
