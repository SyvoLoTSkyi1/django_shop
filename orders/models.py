from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import DiscountTypes

User = get_user_model()


class Discount(PKMixin):
    amount = models.PositiveIntegerField(
        default=0
    )
    code = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(
        default=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )

    def __str__(self):
        return f'{self.code} | {self.amount} | {self.is_active}'


class Order(PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True

    )
    items = models.ManyToManyField(
        "items.Item",
        through='orders.OrderItemRelation'
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user'],
                                               condition=models.Q(is_active=True),
                                               name='unique_is_active')
                       ]

    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def count_total_amount(self):
        if self.discount:
            if self.discount.discount_type == DiscountTypes.VALUE:
                return (self.total_amount - self.discount.amount).quantize(
                    Decimal('.00'))
            elif self.discount.discount_type == DiscountTypes.PERCENT:
                return (self.total_amount - ((
                    self.total_amount * self.discount.amount) / 100)).quantize(
                    Decimal('.00'))  # noqa
        return self.total_amount

    def __str__(self):
        return f'{self.count_total_amount()}'


class OrderItemRelation(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        'items.Item',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'item')
