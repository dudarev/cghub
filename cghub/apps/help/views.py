import logging

from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

from cghub.apps.core.views import AjaxView

from .models import HelpText


hints_logger = logging.getLogger('help.hints')


class HelpView(TemplateView):
    # override it in urls as
    # ... HelpView.as_view(template_name='help/navbar.html') ...
    template_name = 'help/help.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET:
            return HttpResponseRedirect(reverse('help_page'))
        return super(HelpView, self).dispatch(request, *args, **kwargs)


class HelpHintView(AjaxView):

    def get_context_data(self, key):
        text = settings.HELP_HINTS.get(key)
        if text:
            return {'success': True, 'text': text}
        else:
            hints_logger.info('%s key is missing' % key)
            return {'success': False}

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        key = request.GET.get('key')
        context = self.get_context_data(key)
        return self.render_to_response(context)


class HelpTextView(AjaxView):

    def get_context_data(self, slug):
        try:
            help_text = HelpText.objects.get(slug=slug)
        except HelpText.DoesNotExist:
            return {'success': False}
        return {
                'success': True,
                'title': help_text.title,
                'content': help_text.content}

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        slug = request.GET.get('slug')
        context = self.get_context_data(slug)
        return self.render_to_response(context)
