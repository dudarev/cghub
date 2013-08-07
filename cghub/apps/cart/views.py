import datetime
import logging
import time

from operator import itemgetter

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json
from django.utils import timezone
from django.utils.http import cookie_date
from django.utils.importlib import import_module

from cghub.apps.core import browser_text_search
from cghub.apps.core.utils import (
                    get_filters_dict, paginator_params,
                    RequestIDs, RequestDetail)
from cghub.apps.core.attributes import ATTRIBUTES

import cghub.apps.cart.utils as cart_utils
from .forms import SelectedFilesForm, AllFilesForm
from .utils import (
                add_file_to_cart, remove_file_from_cart,
                get_or_create_cart, get_cart_stats, cart_clear,
                load_missing_attributes,
                cart_remove_files_without_attributes,
                add_ids_to_cart, add_files_to_cart)
from .cache import is_cart_cache_exists


cart_logger = logging.getLogger('cart')


def cart_add_selected_files(request):
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
                    try:
                        save_to_cart_cache(analysis_id, last_modified)
                    except AnalysisFileException as e:
                        cart_logger.error(str(e))
            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding to cart: %s' % unicode(e))
    else:
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
            if len(queries) > 1:
                for query in queries:
                    api_request = RequestDetail(query=query)
                    add_files_to_cart(request, api_request.call())
                return {'action': 'redirect', 'redirect': reverse('cart_page')}
            if not queries:
                queries = [filters]
            # add ids to cart
            # TODO(nanvel): This is not required any more
            api_request = RequestIDs(query=queries[0])
            add_ids_to_cart(request, api_request.call())
            # add all attributes in task
            # files will be added immediately
            # check session exists
            try:
                Session.objects.get(session_key=session_key)
            except Session.DoesNotExist:
                return
            # modify session
            cart = get_cart(request)

            for query in queries:
                if query:
                    query = decrease_start_date(query)
                    api_request = RequestDetail(query=query)
                    for result in api_request.call():
                        analysis_id = result['analysis_id']
                        if analysis_id not in cart:
                            return
                        filtered_data = {}
                        for attr in attributes:
                            filtered_data[attr] = result.get(attr)
                        cart[analysis_id] = filtered_data
                        last_modified = result['last_modified']
                        if not is_cart_cache_exists(analysis_id, last_modified):
                            cache_file(analysis_id, last_modified)

            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding all files to cart: %s' % unicode(e))
    else:
        cart_logger.error('AllFilesForm not valid: %s' % unicode(form.errors))


def cart_add_files(request):
    if not request.is_ajax():
        raise Http404
    filters = request.POST.get('filters')
    session_created = request.session.session_key == None
    if session_created:
        request.session.save()
    if filters:
        result = cart_add_all_files(request)
    else:
        result = cart_add_selected_files(request)
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
        cart = get_or_create_cart(self.request).values()
        if sort_by:
            item = sort_by[1:] if sort_by[0] == '-' else sort_by
            cart = sorted(cart, key=itemgetter(item), reverse=sort_by[0] == '-')
        stats = get_cart_stats(self.request)
        offset, limit = paginator_params(self.request)
        # will be saved to cookie in get method
        self.paginator_limit = limit
        return {
            'results': cart[offset:offset + limit],
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


class CartDownloadFilesView(View):
    def post(self, request, action):
        cart = request.session.get('cart')
        if cart and action:
            download = getattr(cart_utils, action)
            return download(cart)
        return HttpResponseRedirect(reverse('cart_page'))
