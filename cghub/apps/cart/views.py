from StringIO import StringIO
from operator import itemgetter
from django.conf import settings
import os
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from cghub.apps.cart.utils import add_file_to_cart, remove_file_from_cart, cache_results
from cghub.apps.cart.utils import get_or_create_cart, get_cart_stats
from django.core.servers import basehttp
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
        return {'results': cart, 'stats': get_cart_stats(self.request)}


class CartAddRemoveFilesView(View):
    """ Handles files added to cart """

    def post(self, request, action):
        if 'add' == action:
            # get all additional attributes of files
            attributes = json.loads(request.POST['attributes'])
            for f in request.POST.getlist('selected_files'):
                add_file_to_cart(request, attributes[f])
                cache_results(attributes[f])
            return HttpResponse(
                json.dumps({"redirect": reverse('cart_page')}),
                mimetype="application/json")
        if 'remove' == action:
            for f in request.POST.getlist('selected_files'):
                # remove file from cart by sample id
                remove_file_from_cart(request, f)
            return HttpResponseRedirect(reverse('cart_page'))


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
        response['Content-Disposition'] = 'attachment; filename=xml.xml'
        return response
