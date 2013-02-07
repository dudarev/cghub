from django.conf.urls import patterns, url
from cghub.apps.cart.views import CartView, CartAddRemoveFilesView, CartDownloadFilesView


urlpatterns = patterns('',
    url(r'^(?P<action>add|add_all|remove)/$', CartAddRemoveFilesView.as_view(), name='cart_add_remove_files'),
    url(r'^(?P<action>manifest|xml)/$', CartDownloadFilesView.as_view(), name='cart_download_files'),
    url(r'^$', CartView.as_view(), name='cart_page'),
)
