from django.conf.urls import patterns, url
from cghub.apps.cart.views import (CartView, CartAddRemoveFilesView,
                                   CartDownloadFilesView, CartClearView)


urlpatterns = patterns('',
    url(
        r'^(?P<action>add|remove)/$',
        CartAddRemoveFilesView.as_view(),
        name='cart_add_remove_files'),
    url(
        r'^clear/$',
        CartClearView.as_view(),
        name='clear_cart'),
    url(
        r'^(?P<action>manifest_xml|manifest_tsv|metadata_xml|metadata_tsv)/$',
        CartDownloadFilesView.as_view(),
        name='cart_download_files'),
    url(r'^$', CartView.as_view(), name='cart_page'),
)
