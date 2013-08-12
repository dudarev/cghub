import logging

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json

from cghub.apps.core import browser_text_search
from cghub.apps.core.utils import (
                    get_filters_dict, paginator_params,
                    RequestDetail, get_results_for_ids)

import cghub.apps.cart.utils as cart_utils
from .forms import SelectedItemsForm, AllItemsForm
from .utils import Cart


cart_logger = logging.getLogger('cart')


def cart_add_selected_files(request):
    form = SelectedItemsForm(request.POST)
    if form.is_valid():
        try:
            cart = Cart(request.session)
            for result in form.cleaned_data['selected_items']:
                cart.add(result)
            cart.update_stats()
            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding to cart: %s' % unicode(e))
    else:
        cart_logger.error('SelectedItemsForm not valid: %s' % unicode(form.errors))


def cart_add_all_files(request):
    # 'Add all to cart' pressed
    form = AllItemsForm(request.POST)
    if form.is_valid():
        try:
            # calculate query
            raw_filters = form.cleaned_data['filters']
            filters = get_filters_dict(raw_filters)
            q = raw_filters.get('q')
            queries = []
            if q:
                # FIXME: temporary hack to work around GNOS not quoting Solr query
                # FIXME: this is temporary hack, need for multiple requests will be fixed at CGHub
                if browser_text_search.useAllMetadataIndex:
                    query = {'all_metadata': browser_text_search.ws_query(q)}
                    query.update(filters)
                    queries = [query]
                else:
                    query = {'xml_text': u"(%s)" % q}
                    query.update(filters)
                    queries = [query, {'analysis_id': q}]
            if not queries:
                queries = [filters]

            cart = Cart(request.session)
            for query in queries:
                api_request = RequestDetail(query=query)
                for result in api_request.call():
                    cart.add(result)
                cart.update_stats()
            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding all files to cart: %s' % unicode(e))
    else:
        cart_logger.error('AllItemsForm not valid: %s' % unicode(form.errors))


def cart_add_files(request):
    if not request.is_ajax():
        raise Http404
    filters = request.POST.get('filters')
    if filters:
        result = cart_add_all_files(request)
    else:
        result = cart_add_selected_files(request)
    result = result or {'action': 'error'}
    return HttpResponse(json.dumps(result), mimetype="application/json")


class CartView(TemplateView):
    """
    Lists files in cart
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request.session)
        offset, limit = paginator_params(self.request)
        # will be saved to cookie in get method
        self.paginator_limit = limit
        return {
            'results': cart.page(offset=offset, limit=limit),
            'num_results': cart.all_count,
            'size': cart.size}

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
            cart = Cart(request.session)
            for analysis_id in request.POST.getlist('selected_files'):
                cart.remove(analysis_id)
            cart.update_stats()
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
        cart = Cart(request.session)
        cart.clear()
        url = reverse('cart_page')
        return HttpResponseRedirect(url)


class CartDownloadFilesView(View):
    def post(self, request, action):
        cart = request.session.get('cart')
        if cart and action:
            download = getattr(cart_utils, action)
            return download(cart)
        return HttpResponseRedirect(reverse('cart_page'))
