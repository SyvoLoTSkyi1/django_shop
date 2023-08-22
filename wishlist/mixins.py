from wishlist.models import Wishlist


class GetWishlistMixin:

    def get_wishlist_object(self):
        return Wishlist.objects.get_or_create(
            user=self.request.user
        )[0]
