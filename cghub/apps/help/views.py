from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect


class HelpSearchView(TemplateView):
    template_name = 'help/search.html'


class HelpCartView(TemplateView):
    template_name = 'help/cart.html'


class HelpMainView(TemplateView):
    template_name = 'help/help.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET:
            if request.GET.get('from', '').startswith('/search'):
                return HttpResponseRedirect(reverse('help_search_page'))
            if request.GET.get('from', '').startswith('/cart'):
                return HttpResponseRedirect(reverse('help_cart_page'))
            return HttpResponseRedirect(reverse('help_page'))
        return super(HelpMainView, self).dispatch(request, *args, **kwargs)