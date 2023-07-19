from django.urls import path, re_path

from orders.views import CartView, UpdateCartView, RecalculateCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    re_path(r'cart/(?P<action>add|remove)/', UpdateCartView.as_view(), name='update_cart'),
    path('recalculate/', RecalculateCartView.as_view(), name='recalculate_cart')
]