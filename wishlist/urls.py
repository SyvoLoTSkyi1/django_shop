from django.urls import path

from wishlist.views import WishlistView, UpdateWishlistView

urlpatterns = [
    path('wishlist/',
         WishlistView.as_view(),
         name='wishlist'),
    path('wishlist/<uuid:pk>/',
         UpdateWishlistView.as_view(),
         name='update_wishlist'),
]
