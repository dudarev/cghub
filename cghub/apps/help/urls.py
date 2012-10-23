from django.conf.urls import patterns, url

from cghub.apps.help.views import HelpView


urlpatterns = patterns(
    '',
    url(r'^$', HelpView.as_view(), name='help_page'),
    url(r'^overview/$',
        HelpView.as_view(template_name='help/overview.html'),
        name='help_overview_page'),
    url(r'^navbar/$',
        HelpView.as_view(template_name='help/navbar.html'),
        name='help_navbar_page'),
    url(r'^results/$',
        HelpView.as_view(template_name='help/results.html'),
        name='help_results_page'),
    url(r'^usecase/$',
        HelpView.as_view(template_name='help/usecase.html'),
        name='help_usecase_page'),
    url(r'^filters/$',
        HelpView.as_view(template_name='help/filters.html'),
        name='help_filters_page'),
    url(r'^cart/$',
        HelpView.as_view(template_name='help/cart.html'),
        name='help_cart_page'),
    # TODO: is it used?
    url(r'^search/$',
        HelpView.as_view(template_name='help/search.html'),
        name='help_search_page'),
)
