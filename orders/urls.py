from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from orders.views import CartView, UpdateCartView, RecalculateCartView, ApplyDiscountView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    re_path(r'cart/(?P<action>add|remove|clear|pay)/',
            login_required(UpdateCartView.as_view()),
            name='update_cart'),
    path('recalculate/',
         login_required(RecalculateCartView.as_view()),
         name='recalculate_cart'),
    path('apply_discount/',
         login_required(ApplyDiscountView.as_view()),
         name='apply_discount'),
]
