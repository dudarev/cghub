import datetime
import logging
from operator import itemgetter

from celery import states
from djcelery.models import TaskState

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json
from django.utils import timezone
from django.utils.http import urlquote

from cghub.apps.core.utils import (is_celery_alive,
                    generate_task_id, get_wsapi_settings,
                    get_filters_string, is_task_done)
from cghub.apps.core.attributes import ATTRIBUTES

from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.utils import (add_file_to_cart, remove_file_from_cart,
                            get_or_create_cart, get_cart_stats, clear_cart,
                            check_missing_files, cache_file,
                            cart_remove_files_without_attributes,
                            add_ids_to_cart, add_files_to_cart)
from cghub.apps.cart.cache import is_cart_cache_exists
from cghub.apps.cart.tasks import add_files_to_cart_by_query_task
import cghub.apps.cart.utils as cart_utils

from cghub.wsapi.api_light import get_all_ids
from cghub.wsapi.api import multiple_request as api_multiple_request
from cghub.wsapi import browser_text_search


WSAPI_SETTINGS = get_wsapi_settings()

cart_logger = logging.getLogger('cart')


def cart_add_selected_files(request, celery_alive):
    form = SelectedFilesForm(request.POST)
    if form.is_valid():
        try:
            attributes = form.cleaned_data['attributes']
            selected_files = request.POST.getlist('selected_files')
            for f in selected_files:
                add_file_to_cart(request, attributes[f])
                analysis_id = attributes[f].get('analysis_id')
                last_modified = attributes[f].get('last_modified')
                if not is_cart_cache_exists(analysis_id, last_modified):
                        cache_file(analysis_id, last_modified, celery_alive)
            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding to cart: %s' % unicode(e))
    else:
        cart_logger.error('SelectedFilesForm not valid: %s' % unicode(form.errors))


def cart_add_all_files(request, celery_alive):
    # 'Add all to cart' pressed
    form = AllFilesForm(request.POST)
    if form.is_valid():
        try:
            # calculate query
            filters = form.cleaned_data['filters']
            filter_str = get_filters_string(filters)
            q = filters.get('q')
            # FIXME: the API should hide all URL quoting and parameters [markd]
            queries = []
            if q:
                # FIXME: temporary hack to work around GNOS not quoting Solr query
                # FIXME: this is temporary hack, need for multiple requests will be fixed at CGHub
                if browser_text_search.useAllMetadataIndex:
                    query = u"all_metadata={0}".format(
                                urlquote(browser_text_search.ws_query(q))) + filter_str
                    queries = [query]
                else:
                    query = u"xml_text={0}".format(urlquote(u"("+q+u")"))
                    query += filter_str
                    queries = [query, u"analysis_id={0}".format(urlquote(q))]
            if len(queries) > 1:
                # add files to cart
                # should be already cached, add immediately
                results = api_multiple_request(queries_list=queries, settings=WSAPI_SETTINGS)
                results.add_custom_fields()
                add_files_to_cart(request, results)
                return {'action': 'redirect', 'redirect': reverse('cart_page')}
            if not queries:
                # remove front ampersand
                queries = [filter_str[1:]]
            # add ids to cart
            ids = get_all_ids(query=queries[0], settings=WSAPI_SETTINGS)
            add_ids_to_cart(request, ids)
            # add all attributes in task
            if celery_alive:
                # check task is already exists
                kwargs = {
                            'data': form.cleaned_data,
                            'session_key': request.session.session_key}
                task_id = generate_task_id(**kwargs)
                request.session['task_id'] = task_id
                request.session.save()
                request.session.modified = False
                try:
                    task = TaskState.objects.get(task_id=task_id)
                    # task already done, reexecute task
                    if task.state not in (states.RECEIVED, states.STARTED):
                        task.state = states.RETRY
                        task.save()
                        add_files_to_cart_by_query_task.apply_async(
                            kwargs={
                                        'queries': queries,
                                        'attributes': ATTRIBUTES,
                                        'session_key': request.session.session_key},
                            task_id=task_id)
                except TaskState.DoesNotExist:
                    # files will be added later by celery task
                    task = TaskState(
                                state=states.RETRY, tstamp=timezone.now(),
                                task_id=task_id)
                    task.save()
                    add_files_to_cart_by_query_task.apply_async(
                            kwargs={
                                    'queries': queries,
                                    'attributes': ATTRIBUTES,
                                    'session_key': request.session.session_key},
                            task_id=task_id)
                return {
                        'action': 'redirect',
                        'redirect': reverse('cart_page'),
                        'task_id': task_id}
            else:
                # files will be added immediately
                add_files_to_cart_by_query_task(
                        queries=queries,
                        attributes=ATTRIBUTES,
                        session_key=request.session.session_key)
                return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding all files to cart: %s' % unicode(e))
    else:
        cart_logger.error('AllFilesForm not valid: %s' % unicode(form.errors))


def cart_add_files(request):
    if not request.is_ajax():
        raise Http404
    filters = request.POST.get('filters')
    celery_alive = is_celery_alive()
    if request.session.session_key == None:
        request.session.save()
    # check that we still working on adding files to cart
    if celery_alive and request.session.get('task_id'):
        result = {
            'action': 'message',
            'title': 'Still adding files to cart',
            'content': 'Please wait, files from your previous request not fully loaded to Your cart'}
    elif filters:
        result = cart_add_all_files(request, celery_alive)
    else:
        result = cart_add_selected_files(request, celery_alive)
    result = result or {'action': 'error'}
    return HttpResponse(json.dumps(result), mimetype="application/json")


class CartView(TemplateView):
    """
    Lists files in cart
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        sort_by = self.request.GET.get('sort_by')
        # check any tasks to add files to cart
        task_id = self.request.session.get('task_id')
        missed_files = 0
        if task_id and is_task_done(task_id):
            # remove task_id from session and remove files with
            # not completely loaded attributes
            # and show error message in case if ones exists
            missed_files = cart_remove_files_without_attributes(
                                                        self.request)
            del self.request.session['task_id']
            self.request.session.save()
        cart = get_or_create_cart(self.request).values()
        if sort_by and not self.request.session.get('task_id'):
            item = sort_by[1:] if sort_by[0] == '-' else sort_by
            cart = sorted(cart, key=itemgetter(item), reverse=sort_by[0] == '-')
        stats = get_cart_stats(self.request)
        offset = self.request.GET.get('offset')
        offset = offset and offset.isdigit() and int(offset) or 0
        limit = self.request.GET.get('limit')
        limit = limit and limit.isdigit() and int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
        """
        Check for not fully added files
        """
        files = check_missing_files(cart[offset:offset + limit])
        self.request.session.modified = False
        return {
            'results': files,
            'stats': stats,
            'missed_files': missed_files,
            'num_results': stats['count']}


class CartAddRemoveFilesView(View):
    """
    Handles files added to cart
    """
    def post(self, request, action):
        if 'add' == action:
            return cart_add_files(request)
        if 'remove' == action:
            for f in request.POST.getlist('selected_files'):
                # remove file from cart by sample id
                remove_file_from_cart(request, f)
            params = request.META.get('HTTP_REFERER', '')
            url = reverse('cart_page')
            if params.find('/?') != -1:
                url += params[params.find('/?') + 1:len(params)]
            return HttpResponseRedirect(url)

    def get(self, request, action):
        raise Http404


class CartClearView(View):
    """
    Handels clearing cart
    """
    def post(self, request):
        clear_cart(request)
        url = reverse('cart_page')
        return HttpResponseRedirect(url)


class CartDownloadFilesView(View):
    def post(self, request, action):
        cart = request.session.get('cart')
        if cart and action:
            download = getattr(cart_utils, action)
            return download(cart)
        return HttpResponseRedirect(reverse('cart_page'))
