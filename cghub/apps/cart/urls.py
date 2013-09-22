from django.conf.urls import patterns, url
from cghub.apps.cart.views import (
                CartAddItem, CartAddRemoveItemsView, CartClearView,
                CartDownloadFilesView, CartView)


urlpatterns = patterns('',
    url(
        r'^(?P<action>add|remove)/$',
        CartAddRemoveItemsView.as_view(), name='cart_add_remove_items'),
    url(
        r'^add/(?P<analysis_id>'
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        CartAddItem.as_view(), name='cart_add_item'),
    url(
        r'^clear/$',
        CartClearView.as_view(), name='cart_clear'),
    url(
        r'^(?P<action>manifest|metadata|summary)/$',
        CartDownloadFilesView.as_view(), name='cart_download_files'),
    url(r'^$', CartView.as_view(), name='cart_page'),
)
