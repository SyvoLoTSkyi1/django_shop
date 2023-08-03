from os import path

from django.core.validators import MinValueValidator
from django.db import models

from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/' \
        f'{instance.pk}/image{extension}'


class Item(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )
    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True)
    image = models.ImageField(upload_to=upload_image)
    category = models.ForeignKey(
        "items.Category",
        on_delete=models.CASCADE
    )
    items = models.ManyToManyField('items.Item', blank=True)

    def __str__(self):
        return f"{self.name} | {self.category}"


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.name
