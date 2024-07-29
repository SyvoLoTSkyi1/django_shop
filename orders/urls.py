from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from orders.views import CartView, UpdateCartView, RecalculateCartView, ApplyDiscountView, OrderConfirmView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    re_path(r'cart/(?P<action>add|remove|clear|pay)/',
            login_required(UpdateCartView.as_view()),
            name='update_cart'),
    path('cart/recalculate/',
         login_required(RecalculateCartView.as_view()),
         name='recalculate_cart'),
    path('cart/apply_discount/',
         login_required(ApplyDiscountView.as_view()),
         name='apply_discount'),
    path('cart/confirmation/',
         OrderConfirmView.as_view(),
         name='cart_confirmation'),

]
