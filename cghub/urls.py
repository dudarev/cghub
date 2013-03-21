from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cghub.apps.core.views import (HomeView, SearchView, ItemDetailsView,
	MetadataView, CeleryTasksView, CeleryTaskStatusView)


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^search/$', SearchView.as_view(), name='search_page'),
    url(r'^details/(?P<uuid>'
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        ItemDetailsView.as_view(), name='item_details'),
    url(r'^metadata/(?P<uuid>'
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        MetadataView.as_view(), name='metadata'),
    url(r'^cart/', include('cghub.apps.cart.urls')),
    url(r'^help/', include('cghub.apps.help.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^status/$', CeleryTasksView.as_view(), name='celery_tasks'),
    url(r'^task/status/$', CeleryTaskStatusView.as_view(), name='celery_task_status'),
)

urlpatterns += staticfiles_urlpatterns()
