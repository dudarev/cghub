from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect


class HelpView(TemplateView):
    template_name = 'help/help.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET:
            if request.GET.get('from', '').startswith('/search'):
                return HttpResponseRedirect(reverse('help_search_page'))
            if request.GET.get('from', '').startswith('/cart'):
                return HttpResponseRedirect(reverse('help_cart_page'))
            return HttpResponseRedirect(reverse('help_page'))
        # use template specified in urls if defined
        self.template_name = kwargs.get('template', self.template_name)
        return super(HelpView, self).dispatch(request, *args, **kwargs)
