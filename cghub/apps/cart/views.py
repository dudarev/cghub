import datetime
import logging
import time
from operator import itemgetter

from celery import states
from djcelery.models import TaskState

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json
from django.utils import timezone
from django.utils.http import cookie_date
from django.utils.importlib import import_module

from cghub.apps.core.utils import (is_celery_alive,
                    generate_task_id, get_wsapi_settings,
                    get_filters_string, is_task_done, paginator_params)
from cghub.apps.core.attributes import ATTRIBUTES

from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.utils import (add_file_to_cart, remove_file_from_cart,
                            get_or_create_cart, get_cart_stats, cart_clear,
                            load_missing_attributes, cache_file,
                            cart_remove_files_without_attributes,
                            add_ids_to_cart, add_files_to_cart)
from cghub.apps.cart.cache import is_cart_cache_exists
from cghub.apps.cart.tasks import add_files_to_cart_by_query_task
import cghub.apps.cart.utils as cart_utils

from cghub.wsapi.api import request_ids
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
            queries = []
            if q:
                # FIXME: temporary hack to work around GNOS not quoting Solr query
                # FIXME: this is temporary hack, need for multiple requests will be fixed at CGHub
                if browser_text_search.useAllMetadataIndex:
                    query = u"all_metadata={0}".format(
                            browser_text_search.ws_query(q)) + filter_str
                    queries = [query]
                else:
                    query = u"xml_text={0}".format(u"("+q+u")")
                    query += filter_str
                    queries = [query, u"analysis_id={0}".format(q)]
            if len(queries) > 1:
                # add files to cart
                # should be already cached, add immediately
                results = api_multiple_request(
                            queries_list=queries, settings=WSAPI_SETTINGS)
                results.add_custom_fields()
                add_files_to_cart(request, results)
                return {'action': 'redirect', 'redirect': reverse('cart_page')}
            if not queries:
                # remove front ampersand
                queries = [filter_str[1:]]
            # add ids to cart
            ids = get_all_ids(
                            query=queries[0], settings=WSAPI_SETTINGS,
                            sort_by=filters.get('sort_by'))
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
                request.session.save()
                request.session.modified = False
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
    session_created = request.session.session_key == None
    if session_created:
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
    response = HttpResponse(json.dumps(result), mimetype="application/json")
    # set session cookie if session was created
    if session_created:
        if request.session.get_expire_at_browser_close():
            max_age = None
            expires = None
        else:
            max_age = request.session.get_expiry_age()
            expires_time = time.time() + max_age
            expires = cookie_date(expires_time)
        response.set_cookie(settings.SESSION_COOKIE_NAME,
                        request.session.session_key, max_age=max_age,
                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        path=settings.SESSION_COOKIE_PATH,
                        secure=settings.SESSION_COOKIE_SECURE or None,
                        httponly=settings.SESSION_COOKIE_HTTPONLY or None)
    return response


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
            
            # reload session
            engine = import_module(settings.SESSION_ENGINE)
            self.request.session = engine.SessionStore(
                                session_key=self.request.session.session_key)
            missed_files = cart_remove_files_without_attributes(self.request)
            # log error if missed files
            if missed_files:
                cart_logger.error(
                        'Attributes for %d files were not added to cart, '
                        'these files were removed from cart.' % missed_files)
            del self.request.session['task_id']
            self.request.session.save()
        cart = get_or_create_cart(self.request).values()
        if sort_by and not self.request.session.get('task_id'):
            item = sort_by[1:] if sort_by[0] == '-' else sort_by
            cart = sorted(cart, key=itemgetter(item), reverse=sort_by[0] == '-')
        stats = get_cart_stats(self.request)
        offset, limit = paginator_params(self.request)
        # will be saved to cookie in get method
        self.paginator_limit = limit
        """
        Check for not fully added files
        """
        # set offset to zero if no results returned
        for offset in (offset, 0):
            files = load_missing_attributes(cart[offset:offset + limit])
            if files:
                break
        self.request.session.modified = False
        return {
            'results': files,
            'stats': stats,
            'missed_files': missed_files,
            'num_results': stats['count']}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        if request.GET and response.status_code == 200:
            response.set_cookie(settings.PAGINATOR_LIMIT_COOKIE,
                    self.paginator_limit,
                    max_age=settings.COOKIE_MAX_AGE,
                    path=reverse('home_page'))
        return response


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
        cart_clear(request)
        url = reverse('cart_page')
        return HttpResponseRedirect(url)


class CartTerminateView(View):
    """
    Revokes task to add files to cart and redirects to cart page
    """
    def get(self, request):
        task_id = request.session.get('task_id', None)
        if task_id:
            # Don't use celery.task.control.revoke here because of
            # workers will keep this task_id in memory an ensure that it does not run,
            # so we will not able to restart task until celeryd restart
            try:
                ts = TaskState.objects.get(task_id=task_id)
                ts.state = states.REVOKED
                ts.save()
            except TaskState.DoesNotExist:
                pass
            # task_id will be removed in cart view
        url = reverse('cart_page')
        return HttpResponseRedirect(url)


class CartDownloadFilesView(View):
    def post(self, request, action):
        cart = request.session.get('cart')
        if cart and action:
            download = getattr(cart_utils, action)
            return download(cart)
        return HttpResponseRedirect(reverse('cart_page'))
