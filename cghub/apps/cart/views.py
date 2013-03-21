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
                    generate_task_uuid, get_wsapi_settings)

from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.utils import (add_file_to_cart, remove_file_from_cart,
                                   cache_results, get_or_create_cart,
                                   get_cart_stats, clear_cart)
from cghub.apps.cart.tasks import add_files_to_cart_by_query
import cghub.apps.core.utils as utils

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
        form = AllFilesForm(request.POST)
        if form.is_valid():
            if celery_alive:
                # check task is already exists
                if request.session.session_key == None:
                    request.session.save()
                kwargs = {
                        'data': form.cleaned_data,
                        'session_key': request.session.session_key}
                task_id = generate_task_uuid(**kwargs)
                try:
                    task = TaskState.objects.get(task_id=task_id)
                    # task already done, reexecute task
                    if task.state not in (states.RECEIVED, states.STARTED):
                        add_files_to_cart_by_query.apply_async(
                            kwargs=kwargs,
                            task_id=task_id)
                except TaskState.DoesNotExist:
                    # files will be added later by celery task
                    add_files_to_cart_by_query.apply_async(
                            kwargs=kwargs,
                            task_id=task_id)
                result = {
                            'action': 'message',
                            'task_id': task_id,
                            'content': WILL_BE_ADDED_SOON_CONTENT,
                            'title': WILL_BE_ADDED_SOON_TITLE}
            else:
                # files will be added immediately
                add_files_to_cart_by_query(
                        form.cleaned_data,
                        request.session.session_key)
                result = {'action': 'redirect', 'redirect': reverse('cart_page')}
    else:
        form = SelectedFilesForm(request.POST)
        if form.is_valid():
            attributes = form.cleaned_data['attributes']
            selected_files = request.POST.getlist('selected_files')
            for f in selected_files:
                add_file_to_cart(request, attributes[f])
                if celery_alive:
                    cache_results(attributes[f])
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
        return {
            'results': cart[offset:offset + limit],
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
            download = getattr(utils, action)
            return download(cart)
        return HttpResponseRedirect(reverse('cart_page'))
