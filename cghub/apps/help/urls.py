from django.conf.urls import patterns, url

from cghub.apps.help.views import HelpView, HelpHintView, HelpTextView

urlpatterns = patterns(
    '',
    url(r'^$', HelpView.as_view(), name='help_page'),
    url(r'^overview/$',
        HelpView.as_view(template_name='help/overview.html'),
        name='help_overview_page'),
    url(r'^flow/$',
        HelpView.as_view(template_name='help/flow.html'),
        name='help_flow_page'),
    url(r'^assemblies/$',
        HelpView.as_view(template_name='help/assemblies.html'),
        name='help_assemblies_page'),
    url(r'^hint/$', HelpHintView.as_view(), name='help_hint'),
    url(r'^text/$', HelpTextView.as_view(), name='help_text'),
)
