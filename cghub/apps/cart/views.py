from operator import itemgetter

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json
from django.utils.http import urlquote

from cghub.apps.core.utils import (get_filters_string, is_celery_alive,
                                   get_wsapi_settings, manifest, metadata)
from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.utils import (add_file_to_cart, remove_file_from_cart,
                    cache_results, get_or_create_cart, get_cart_stats)
from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import multiple_request as api_multiple_request
from cghub.wsapi.api import Results


WSAPI_SETTINGS = get_wsapi_settings()


def cart_add_files(request):
    result = {'success': True, 'redirect': reverse('cart_page')}
    if not request.is_ajax():
        raise Http404
    filters = request.POST.get('filters')
    celery_alive = is_celery_alive()
    if filters:
        form = AllFilesForm(request.POST)
        if form.is_valid():
            attributes = form.cleaned_data['attributes']
            filters = form.cleaned_data['filters']
            filter_str = get_filters_string(filters)
            q = filters.get('q')
            if q:
                query = u"xml_text={0}".format(urlquote(q))
                query += filter_str
            else:
                query = filter_str[1:]  # remove front ampersand
            if 'xml_text' in query:
                queries_list = [query, query.replace('xml_text', 'analysis_id', 1)]
                results = api_multiple_request(queries_list=queries_list,
                                    settings=WSAPI_SETTINGS)
            else:
                results = api_request(query=query, settings=WSAPI_SETTINGS)
            results.add_custom_fields()
            if hasattr(results, 'Result'):
                for r in results.Result:
                    r_attrs = dict(
                        (attr, unicode(getattr(r, attr)))
                        for attr in attributes if hasattr(r, attr))
                    r_attrs['files_size'] = int(r.files_size)
                    r_attrs['analysis_id'] = unicode(r.analysis_id)
                    add_file_to_cart(request, r_attrs)
                    if celery_alive:
                        cache_results(r_attrs)
        else:
            result = {'success': False}
    else:
        form = SelectedFilesForm(request.POST)
        if form.is_valid():
            attributes = form.cleaned_data['attributes']
            selected_files = request.POST.getlist('selected_files')
            for f in selected_files:
                add_file_to_cart(request, attributes[f])
                if celery_alive:
                    cache_results(attributes[f])
        else:
            result = {'success': False}
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


class CartDownloadFilesView(View):
    def post(self, request, action):
        cart = request.session.get('cart')
        if cart and action:
            if action.startswith('manifest'):
                return manifest(ids=cart, format=action.split('_')[1])
            if action.startswith('metadata'):
                return metadata(ids=cart, format=action.split('_')[1])
        return HttpResponseRedirect(reverse('cart_page'))
