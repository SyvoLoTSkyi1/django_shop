from django.contrib.auth.mixins import LoginRequiredMixin

from wishlist.models import Wishlist


class GetWishlistMixin(LoginRequiredMixin):

    def get_wishlist_object(self):
        return Wishlist.objects.get_or_create(
            user=self.request.user
        )[0]
