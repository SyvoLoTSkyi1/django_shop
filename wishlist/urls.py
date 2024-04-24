from django.urls import path

from wishlist.views import WishlistView, AjaxUpdateWishlistView

urlpatterns = [
    path('wishlist/',
         WishlistView.as_view(),
         name='wishlist'),
    # path('wishlist/<uuid:pk>/',
    #      UpdateWishlistView.as_view(),
    #      name='update_wishlist'),
    path('ajax-wishlist/<uuid:pk>/',
         AjaxUpdateWishlistView.as_view(),
         name='ajax_update_wishlist'),
]
