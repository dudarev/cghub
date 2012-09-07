from django.conf.urls import patterns, url

from cghub.apps.help.views import (HelpMainView,
        HelpSearchView, HelpCartView)


urlpatterns = patterns('',
    url(r'^$', HelpMainView.as_view(), name='help_page'),
    url(r'^search/$', HelpSearchView.as_view(), name='help_search_page'),
    url(r'^cart/$', HelpCartView.as_view(), name='help_cart_page'),
)
