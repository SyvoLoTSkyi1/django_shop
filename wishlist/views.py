from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from wishlist.forms import UpdateWishlistForm
from wishlist.mixins import GetWishlistMixin


class WishlistView(GetWishlistMixin, TemplateView):
    template_name = 'wishlist/items_wishlist.html'

    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        context.update({
            'wishlist': self.get_wishlist_object()
        })
        return context


class UpdateWishlistView(GetWishlistMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        form = UpdateWishlistForm(request.POST, instance=self.get_wishlist_object())
        if form.is_valid():
            if kwargs['action'] == 'remove':
                messages.warning(request, message='Item was deleted from your wishlist!')
            else:
                messages.success(request, message='Item was add to your wishlist!')
            form.save(kwargs.get('action'))
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'wishlist')
