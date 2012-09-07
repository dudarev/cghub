from django.conf.urls import patterns, url

from cghub.apps.help.views import HelpMainView


urlpatterns = patterns('',
    url(r'^$', HelpMainView.as_view(), name='help_page'),
)
