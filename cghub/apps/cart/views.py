from StringIO import StringIO
from lxml import etree
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from cghub.apps.cart.utils import add_file_to_cart, remove_file_from_cart
from cghub.apps.cart.utils import get_or_create_cart, get_cart_stats
from django.core.servers import basehttp
from cghub.cghub_api.api import request as api_request

class CartView(TemplateView):
    """ Lists files in cart """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        return {'results': get_or_create_cart(self.request),
                'stats': get_cart_stats(self.request)
        }


class CartAddRemoveFilesView(View):
    """ Handles files added to cart """

    def post(self, request, action):
        if 'add' == action:
            # get all additional attributes of files
            attributes = json.loads(request.POST['attributes'])
            for f in request.POST.getlist('selected_files'):
                add_file_to_cart(request, attributes[f])
            return HttpResponse(json.dumps({"redirect": reverse('cart_page')}), mimetype="application/json")
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

    def manifest(self, cart):
        mfio = StringIO()
        results = None
        results_counter = 0
        for file in cart:
            result = api_request(query='analysis_id={0}'.format(file.get('analysis_id')), attributes=False)
            results_counter += 1
            if not results:
                results = result
                results.Query.clear()
                results.Hits.clear()
            else:
                result.Result.set('id', u'{0}'.format(results_counter))
            results.insert(results_counter + 1, result.Result)
        mfio.write(etree.tostring(results))
        mfio.seek(0)
        response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=manifest.xml'
        return response


    def xml(self, cart):
        mfio = StringIO()
        mfio.write('<root>TEST XML FILE</root>')
        mfio.seek(0)
        response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=xml.xml'
        return response
