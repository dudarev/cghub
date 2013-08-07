import logging

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json

from cghub.apps.core import browser_text_search
from cghub.apps.core.utils import (
                    get_filters_dict, paginator_params,
                    RequestIDs, get_results_for_ids)

import cghub.apps.cart.utils as cart_utils
from .forms import SelectedFilesForm, AllFilesForm
from .utils import get_or_create_cart, get_cart_stats, cart_clear


cart_logger = logging.getLogger('cart')


def cart_add_selected_files(request):
    form = SelectedFilesForm(request.POST)
    if form.is_valid():
        try:
            cart = get_or_create_cart(request)
            for analysis_id in form.cleaned_data['selected_items']:
                cart[analysis_id] = {'analysis_id': analysis_id}
            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding to cart: %s' % unicode(e))
    else:
        print form.errors
        cart_logger.error('SelectedFilesForm not valid: %s' % unicode(form.errors))


def cart_add_all_files(request):
    # 'Add all to cart' pressed
    form = AllFilesForm(request.POST)
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

            cart = get_or_create_cart(request)
            for query in queries:
                api_request = RequestIDs(query=query)
                for result in api_request.call():
                    analysis_id = result['analysis_id']
                    cart[analysis_id] = {'analysis_id': analysis_id}

            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding all files to cart: %s' % unicode(e))
    else:
        cart_logger.error('AllFilesForm not valid: %s' % unicode(form.errors))


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
        cart = get_or_create_cart(self.request).keys()
        stats = get_cart_stats(self.request)
        offset, limit = paginator_params(self.request)
        # will be saved to cookie in get method
        self.paginator_limit = limit
        results = get_results_for_ids(cart[offset:offset + limit])
        return {
            'results': results,
            'stats': stats,
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
            cart = get_or_create_cart(request)
            for analysis_id in request.POST.getlist('selected_files'):
                del cart[analysis_id]
            request.session.modified = True
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


class CartDownloadFilesView(View):
    def post(self, request, action):
        cart = request.session.get('cart')
        if cart and action:
            download = getattr(cart_utils, action)
            return download(cart)
        return HttpResponseRedirect(reverse('cart_page'))
