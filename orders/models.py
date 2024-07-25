import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, When, Case, Sum
from django_lifecycle import LifecycleModelMixin, \
    hook, AFTER_UPDATE, BEFORE_UPDATE

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import DiscountTypes

User = get_user_model()


class Discount(PKMixin):
    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
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
        return f"{self.amount} | {self.code} | " \
               f"{DiscountTypes(self.discount_type).label} " \
               f"| {self.is_active}"


class Order(LifecycleModelMixin, PKMixin):
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
        constraints = [models.UniqueConstraint(
            fields=['user'],
            condition=models.Q(is_active=True),
            name='unique_is_active')
        ]

    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def get_items_through(self):
        return self.items.through.objects \
            .filter(order=self) \
            .select_related('item') \
            .annotate(full_price=F('item__price') * F('quantity'))

    def get_total_amount(self):
        total_amount = 0
        for item_relation in self.get_items_through().iterator():
            total_amount += item_relation.full_price

        if self.discount:
            total_amount = (
                total_amount - self.discount.amount
                if self.discount.discount_type == DiscountTypes.VALUE else
                total_amount - (
                        self.total_amount / 100 * self.discount.amount
                )
            ).quantize(decimal.Decimal('.01'))
        return total_amount

    # def get_total_amount(self):
    #     return self.items.through.objects.annotate(
    #         full_price=F('item__price') * F('quantity')
    #     ).aggregate(
    #         total_amount=Case(
    #             When(
    #                 order__discount__discount_type=DiscountTypes.VALUE,
    #                 then=Sum('full_price') - F('order__discount__amount')
    #             ),
    #             When(
    #                 order__discount__discount_type=DiscountTypes.PERCENT,
    #                 then=Sum('full_price') - (
    #                         Sum('full_price'
    #                             ) * F('order__discount__amount') / 100
    #                 )
    #             ),
    #             default=Sum('full_price'),
    #             output_field=models.DecimalField()
    #         )
    #     ).get('total_amount') or 0

    @hook(AFTER_UPDATE)
    def order_after_update(self):
        if self.items.exists():
            self.total_amount = self.get_total_amount()
            self.save(update_fields=('total_amount',), skip_hooks=True)

    @hook(BEFORE_UPDATE, when='is_paid', has_changed=True, was=False)
    def order_is_paid(self):
        self.is_active = False

    def pay(self):
        self.is_paid = True
        self.save()


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
