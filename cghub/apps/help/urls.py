from django.conf.urls import patterns, url

from cghub.apps.help.views import HelpView


urlpatterns = patterns('',
    url(r'^$', HelpView.as_view(), name='help_page'),
    url(r'^search/$', HelpView.as_view(), name='help_search_page',
                                kwargs={'template': 'help/search.html'}),
    url(r'^cart/$', HelpView.as_view(), name='help_cart_page',
                                kwargs={'template': 'help/cart.html'}),
)
