import logging

from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.views.generic.base import View, TemplateView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings


missing_hints_logger = logging.getLogger('help.missed_hints')
missing_hints_logger.addHandler(logging.FileHandler(settings.HELP_LOGGING_FILE))


class HelpView(TemplateView):
    # override it in urls as
    # ... HelpView.as_view(template_name='help/navbar.html') ...
    template_name = 'help/help.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET:
            if request.GET.get('from', '').startswith('/search'):
                return HttpResponseRedirect(reverse('help_search_page'))
            if request.GET.get('from', '').startswith('/cart'):
                return HttpResponseRedirect(reverse('help_cart_page'))
            return HttpResponseRedirect(reverse('help_page'))
        return super(HelpView, self).dispatch(request, *args, **kwargs)


class HelpHintView(View):

    http_method_names = ['get']
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(json.dumps(context), **response_kwargs)

    def get_context_data(self, key):
        text = settings.HELP_HINTS.get(key)
        if text:
            return {'success': True, 'text': text}
        else:
            missing_hints_logger.info('%s key is missing' % key)
            return {'success': False}

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        key = request.GET.get('key')
        context = self.get_context_data(key)
        return self.render_to_response(context)
