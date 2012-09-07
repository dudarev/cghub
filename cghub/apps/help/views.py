from django.views.generic.base import TemplateView

class HelpMainView(TemplateView):
    template_name = 'help/help.html'
