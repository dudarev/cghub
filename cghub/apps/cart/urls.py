from django.conf.urls import patterns, url
from cghub.apps.cart.views import (
                CartView, CartAddRemoveFilesView,
                CartDownloadFilesView, CartClearView)


urlpatterns = patterns('',
    url(
        r'^(?P<action>add|remove)/$',
        CartAddRemoveFilesView.as_view(), name='cart_add_remove_files'),
    url(
        r'^clear/$',
        CartClearView.as_view(), name='cart_clear'),
    url(
        r'^(?P<action>manifest|metadata|summary)/$',
        CartDownloadFilesView.as_view(), name='cart_download_files'),
    url(r'^$', CartView.as_view(), name='cart_page'),
)
