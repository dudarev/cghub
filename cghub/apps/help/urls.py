from django.conf.urls import patterns, url

from cghub.apps.help.views import HelpView


urlpatterns = patterns('',
    url(r'^$', HelpView.as_view(), name='help_page'),
    url(r'^overview/$', HelpView.as_view(), name='help_overview_page',
                                kwargs={'template': 'help/overview.html'}),
    url(r'^navbar/$', HelpView.as_view(), name='help_navbar_page',
                                kwargs={'template': 'help/navbar.html'}),
    url(r'^results/$', HelpView.as_view(), name='help_results_page',
                                kwargs={'template': 'help/results.html'}),
    url(r'^usecase/$', HelpView.as_view(), name='help_usecase_page',
                                kwargs={'template': 'help/usecase.html'}),
    url(r'^filters/$', HelpView.as_view(), name='help_filters_page',
                                kwargs={'template': 'help/filters.html'}),
    url(r'^cart/$', HelpView.as_view(), name='help_cart_page',
                                kwargs={'template': 'help/cart.html'}),
    # TODO: is it used?
    url(r'^search/$', HelpView.as_view(), name='help_search_page',
                                kwargs={'template': 'help/search.html'}),
)
