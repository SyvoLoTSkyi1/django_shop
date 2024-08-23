from os import path

from django.core.cache import cache
from django.db import models
from django_lifecycle import hook, AFTER_CREATE, AFTER_UPDATE

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/' \
        f'{instance.pk}/image{extension}'


class Item(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    actual_price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )
    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to=upload_image,
        default='static/images/products/no_image.jpg'
    )
    size = models.ManyToManyField(
        'items.Size',
        related_name='items',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        "items.Category",
        on_delete=models.CASCADE
    )
    items = models.ManyToManyField('items.Item', blank=True)

    _items_cache_key = 'items'

    def __str__(self):
        return f"{self.name} | {self.category}| {self.sku}"

    @property
    def _item_cache_key(self):
        return f'item_{self.id}'

    @classmethod
    def get_items(cls):
        items = cache.get(cls._items_cache_key)
        print('BEFORE ', items)
        if not items:
            items = Item.objects.all()
            cache.set(cls._items_cache_key, items)
            print('AFTER ', items)
        return items

    @hook(AFTER_CREATE)
    def order_after_create(self):
        cache.delete(self._items_cache_key)

    @hook(AFTER_UPDATE)
    def order_after_update(self):
        cache.delete(self._item_cache_key)


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.name


class PopularItem(PKMixin):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='in_popular'
    )


class Size(PKMixin):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
