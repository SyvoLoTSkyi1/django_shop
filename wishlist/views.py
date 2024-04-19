from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, DetailView, ListView

from items.models import Item
from wishlist.forms import UpdateWishlistForm
from wishlist.mixins import GetWishlistMixin
from wishlist.models import WishlistItem


# class WishlistView(GetWishlistMixin, TemplateView):
#     template_name = 'wishlist/items_wishlist.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(WishlistView, self).get_context_data(**kwargs)
#         context.update({
#             'wishlist': self.get_wishlist_object()
#         })
#         return context


# class UpdateWishlistView(GetWishlistMixin, RedirectView):
#
#     def post(self, request, *args, **kwargs):
#         form = UpdateWishlistForm(request.POST,
#                                   instance=self.get_wishlist_object())
#         if form.is_valid():
#             if kwargs['action'] == 'remove':
#                 messages.warning(request,
#                                  message='Item was deleted from your wishlist!'
#                                  )
#             else:
#                 messages.success(request,
#                                  message='Item was add to your wishlist!')
#             form.save(kwargs.get('action'))
#         return self.get(request, *args, **kwargs)
#
#     def get_redirect_url(self, *args, **kwargs):
#         return reverse_lazy(
#             'wishlist')


class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = 'wishlist/items_wishlist.html'

    # def get_context_data(self, **kwargs):
    #     context = super(WishlistView, self).get_context_data(**kwargs)
    #     context.update({
    #         'wishlist': self.get_wishlist_object()
    #     })
    #     return context


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
        return HttpResponseRedirect(reverse_lazy('items'))
