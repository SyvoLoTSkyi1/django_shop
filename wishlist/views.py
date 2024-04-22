from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from items.models import Item
from wishlist.models import WishlistItem


class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = 'wishlist/items_wishlist.html'


class UpdateWishlistView(LoginRequiredMixin, DetailView):
    model = Item
    template_name_suffix = '_wishlist'

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        user = request.user
        wishlist, created = WishlistItem.objects.get_or_create(
            item=item,
            user=user
        )
        if not created:
            wishlist.delete()
            messages.warning(request,
                            message='Item was deleted from your wishlist!')
        else:
            messages.success(request,
                            message='Item was add to your wishlist!')
        return HttpResponseRedirect(reverse_lazy('items'))
