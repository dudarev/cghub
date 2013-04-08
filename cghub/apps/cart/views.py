import datetime
from operator import itemgetter

from celery import states
from djcelery.models import TaskState

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json
from django.utils.http import urlquote

from cghub.apps.core.utils import (is_celery_alive,
                    generate_task_analysis_id, get_wsapi_settings,
                    get_filters_string)
from cghub.apps.core.attributes import ATTRIBUTES

from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.utils import (add_file_to_cart, remove_file_from_cart,
                            get_or_create_cart, get_cart_stats, clear_cart,
                                                    check_missing_files)
from cghub.apps.cart.cache import is_cart_cache_exists
from cghub.apps.cart.tasks import (add_files_to_cart_by_query_task,
                                                    cache_results_task)
import cghub.apps.cart.utils as cart_utils

from cghub.wsapi.api_light import get_all_ids


WSAPI_SETTINGS = get_wsapi_settings()


def cart_add_files(request):
    WILL_BE_ADDED_SOON_CONTENT = 'Files will be added to your cart soon.'
    WILL_BE_ADDED_SOON_TITLE = 'Message'
    result = {'action': 'error'}
    if not request.is_ajax():
        raise Http404
    filters = request.POST.get('filters')
    celery_alive = is_celery_alive()
    if filters:
        # 'Add all to cart' pressed
        form = AllFilesForm(request.POST)
        if form.is_valid():
            # calculate query
            filters = form.cleaned_data['filters']
            filter_str = get_filters_string(filters)
            q = filters.get('q')
            if q:
                query = u"xml_text={0}".format(urlquote(q))
                query += filter_str
                queries = [query, query.replace('xml_text', 'analysis_id', 1)]
            else:
                query = filter_str[1:]  # remove front ampersand
                queries = [query]
            # add all attributes in task
            if celery_alive:
                # add ids to cart
                for query in queries:
                    ids = get_all_ids(query=query, settings=WSAPI_SETTINGS)
                    cart_utils.add_ids_to_cart(request, ids)
                # check task is already exists
                if request.session.session_key == None:
                    request.session.save()
                kwargs = {
                        'data': form.cleaned_data,
                        'session_key': request.session.session_key}
                task_id = generate_task_analysis_id(**kwargs)
                try:
                    task = TaskState.objects.get(task_id=task_id)
                    # task already done, reexecute task
                    if task.state not in (states.RECEIVED, states.STARTED):
                        add_files_to_cart_by_query_task.apply_async(
                            kwargs={
                                    'queries': queries,
                                    'attributes': ATTRIBUTES,
                                    'session_key': request.session.session_key},
                            task_id=task_id)
                except TaskState.DoesNotExist:
                    # files will be added later by celery task
                    add_files_to_cart_by_query_task.apply_async(
                            kwargs={
                                    'queries': queries,
                                    'attributes': ATTRIBUTES,
                                    'session_key': request.session.session_key},
                            task_id=task_id)
                result = {
                            'action': 'redirect',
                            'redirect': reverse('cart_page'),
                            'task_id': task_id}
            else:
                # files will be added immediately
                add_files_to_cart_by_query_task(
                        queries=queries,
                        attributes=ATTRIBUTES,
                        session_key=request.session.session_key)
                result = {'action': 'redirect', 'redirect': reverse('cart_page')}
    else:
        form = SelectedFilesForm(request.POST)
        if form.is_valid():
            attributes = form.cleaned_data['attributes']
            selected_files = request.POST.getlist('selected_files')
            for f in selected_files:
                add_file_to_cart(request, attributes[f])
                analysis_id = attributes[f].get('analysis_id')
                last_modified = attributes[f].get('last_modified')
                if not is_cart_cache_exists(analysis_id, last_modified):
                    if celery_alive:
                        cache_results_task.delay(analysis_id, last_modified)
                    else:
                        cache_results_task(analysis_id, last_modified)
            result = {'action': 'redirect', 'redirect': reverse('cart_page')}
    return HttpResponse(json.dumps(result), mimetype="application/json")


class CartView(TemplateView):
    """
    Lists files in cart
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        sort_by = self.request.GET.get('sort_by')
        cart = get_or_create_cart(self.request).values()
        if sort_by:
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
        return {
            'results': files,
            'stats': stats,
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
