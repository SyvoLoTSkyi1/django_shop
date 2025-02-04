from django.contrib.auth import get_user_model
from django.db import models

from items.models import Item
from shop.mixins.models_mixins import PKMixin


class WishlistItem(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='in_wishlist'
    )

    class Meta:
        unique_together = ('user', 'item')
