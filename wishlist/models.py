from django.contrib.auth import get_user_model
from django.db import models

from items.models import Item
from shop.mixins.models_mixins import PKMixin


class Wishlist(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField(Item)
