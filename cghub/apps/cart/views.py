from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from cghub.apps.cart.utils import add_file_to_cart, remove_file_from_cart
from cghub.apps.cart.utils import get_or_create_cart, get_cart_stats


class CartView(TemplateView):
    """ Lists files in cart """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        return {'results': get_or_create_cart(self.request),
            'stats': get_cart_stats(self.request)
        }

class CartAddRemoveFilesView(TemplateView):
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
        