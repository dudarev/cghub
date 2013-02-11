import os
from StringIO import StringIO
from operator import itemgetter

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.core.servers import basehttp
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json

from cghub.apps.core.utils import get_filters_string
from cghub.apps.cart.utils import add_file_to_cart, remove_file_from_cart, cache_results
from cghub.apps.cart.utils import get_or_create_cart, get_cart_stats
from cghub.apps.core.forms import CheckInputTypeForm
from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import Results


class CartView(TemplateView):
    """ Lists files in cart """
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
    """ Handles files added to cart """

    def post(self, request, action):
        if 'add' == action:
            if not request.is_ajax():
                raise Http404
            filters = request.POST.get('filters')
            attributes = request.POST.get('attributes')
            type_form = CheckInputTypeForm(filters, attributes)
            if type_form.is_valid():
                attributes = type_form.cleaned_data['attributes']
                filters = type_form.cleaned_data['filters']
                if filters:
                    attributes = json.loads(attributes)
                    filters = json.loads(filters)
                    query = get_filters_string(filters)[1:]
                    results = api_request(query=query)
                    results.add_custom_fields()
                    for r in results.Result:
                        r_attrs = dict(
                            (attr, unicode(getattr(r, attr)))
                            for attr in attributes if hasattr(r, attr))
                        r_attrs['files_size'] = int(r.files_size)
                        r_attrs['analysis_id'] = unicode(r.analysis_id)
                        add_file_to_cart(request, r_attrs)
                        cache_results(r_attrs)
                else:
                    attributes = json.loads(request.POST.get('attributes'))
                    for f in request.POST.getlist('selected_files'):
                        add_file_to_cart(request, attributes[f])
                        cache_results(attributes[f])
                return HttpResponse(
                    json.dumps({"redirect": reverse('cart_page')}),
                    mimetype="application/json")
            else:
                return HttpResponse(
                    json.dumps({"success": "False"}),
                    mimetype="application/json")
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
        if cart and hasattr(self, action):
            download = getattr(self, action)
            return download(cart)
        else:
            return HttpResponseRedirect(reverse('cart_page'))

    @staticmethod
    def get_results(cart, get_attributes):
        results = None
        results_counter = 1
        for analysis_id in cart:
            filename = "{0}_with{1}_attributes".format(
                analysis_id,
                '' if get_attributes else 'out')
            try:
                result = Results.from_file(os.path.join(settings.CART_CACHE_FOLDER, filename))
            except IOError:
                result = api_request(
                    query='analysis_id={0}'.format(analysis_id),
                    get_attributes=get_attributes)
            if results is None:
                results = result
                results.Query.clear()
                results.Hits.clear()
            else:
                result.Result.set('id', u'{0}'.format(results_counter))
                # '+ 1' because the first two elements (0th and 1st) are Query and Hits
                results.insert(results_counter + 1, result.Result)
            results_counter += 1
        return results

    def manifest(self, cart):
        mfio = StringIO()
        results = self.get_results(cart, get_attributes=False)
        mfio.write(results.tostring())
        mfio.seek(0)
        response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=manifest.xml'
        return response

    def xml(self, cart):
        mfio = StringIO()
        results = self.get_results(cart, get_attributes=True)
        mfio.write(results.tostring())
        mfio.seek(0)
        response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=metadata.xml'
        return response
