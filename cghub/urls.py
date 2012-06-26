from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cghub.apps.core.views import HomeView, SearchView, HelpView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^search/$', SearchView.as_view(), name='search_page'),
    url(r'^cart/', include('cghub.apps.cart.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^help/$', HelpView.as_view(), name='help_page'),
)

urlpatterns += staticfiles_urlpatterns()
