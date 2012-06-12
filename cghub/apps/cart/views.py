from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from cghub.apps.cart.utils import add_file_to_cart, remove_file_from_cart
from cghub.apps.cart.utils import get_or_create_cart, get_cart_stats


class CartView(TemplateView):
    """ Lists files in cart """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        return {'cart': get_or_create_cart(self.request),
            'stats': get_cart_stats(self.request)
        }

class CartAddRemoveFilesView(TemplateView):
    """ Handles files added to cart """
    def post(self, request, action):
        for f in request.POST.getlist('selected_files'):
            if "add" == action:
                add_file_to_cart(request, f)
            if "remove" == action:
                remove_file_from_cart(request, f)
        return HttpResponseRedirect(reverse('cart_page'))