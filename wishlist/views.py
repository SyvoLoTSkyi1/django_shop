# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
# from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from items.models import Item
from shop.decorators import ajax_required
from wishlist.models import WishlistItem


class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = 'wishlist/items_wishlist.html'


# class UpdateWishlistView(LoginRequiredMixin, DetailView):
#     model = Item
#     template_name_suffix = '_wishlist'
#
#     def get(self, request, *args, **kwargs):
#         item = self.get_object()
#         user = request.user
#         wishlist, created = WishlistItem.objects.get_or_create(
#             item=item,
#             user=user
#         )
#         if not created:
#             wishlist.delete()
#             messages.warning(request,
#                             message='Item was deleted from your wishlist!')
#         else:
#             messages.success(request,
#                             message='Item was add to your wishlist!')
#         return HttpResponseRedirect(reverse_lazy('items'))


class AjaxUpdateWishlistView(LoginRequiredMixin, DetailView):
    model = Item

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        user = request.user
        wishlist, created = WishlistItem.objects.get_or_create(
            item=item,
            user=user
        )
        if not created:
            wishlist.delete()

        return JsonResponse({'created': created})
