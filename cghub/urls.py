from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cghub.apps.core.views import (
            HomeView, SearchView, BatchSearchView,
            ItemDetailsView, MetadataView)


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^search/$', SearchView.as_view(), name='search_page'),
    url(r'^search/batch/$', BatchSearchView.as_view(), name='batch_search_page'),
    url(r'^details/(?P<analysis_id>'
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        ItemDetailsView.as_view(), name='item_details'),
    url(r'^metadata/(?P<analysis_id>'
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        MetadataView.as_view(), name='metadata'),
    url(r'^cart/', include('cghub.apps.cart.urls')),
    url(r'^help/', include('cghub.apps.help.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.generic.simple',
    url(
        r'^accessibility/$', 'direct_to_template',
        {'template': 'help/accessibility.html'}, name='accessibility_page'),
)

urlpatterns += staticfiles_urlpatterns()

handler500 = 'cghub.apps.core.views.error_500'
