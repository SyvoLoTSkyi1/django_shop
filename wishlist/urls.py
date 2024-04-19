from django.urls import path, re_path

from wishlist.views import WishlistView, UpdateWishlistView

urlpatterns = [
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    # re_path(r'wishlist/(?P<action>add|remove)/',
    #         UpdateWishlistView.as_view(),
    #         name='update_wishlist'),
    path('wishlist/<uuid:pk>/',
         UpdateWishlistView.as_view(),
         name='update_wishlist'),
]
