from django.conf.urls import patterns, url
from cghub.apps.cart.views import CartView, CartAddRemoveFilesView


urlpatterns = patterns('',
    url(r'^(?P<action>add|remove)/$',
        CartAddRemoveFilesView.as_view(),
        name='cart_add_remove_files'),
    url(r'^$', CartView.as_view(), name='cart_page'),
)
