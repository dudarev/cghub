from django.conf.urls import patterns, url
from cghub.apps.cart.views import CartView


urlpatterns = patterns('',
    url(r'^$', CartView.as_view(), name='cart_page'),
)
