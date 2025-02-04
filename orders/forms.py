from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from items.models import Item, Size
from orders.models import Discount, OrderItemRelation


class UpdateCartOrderForm(forms.Form):
    item = forms.UUIDField(required=False)
    size = forms.ModelChoiceField(queryset=Size.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']
        self.action = kwargs['action']

    def clean(self):

        item_id = self.cleaned_data['item']
        size = self.cleaned_data['size']

        if self.action == 'add':
            if not item_id:
                raise ValidationError('Item is required for this action.')
            if not size:
                raise ValidationError('Size is required for this action.')

        if item_id:
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                raise ValidationError('Wrong item id.')

            if size and size not in item.size.all():
                raise ValidationError(
                    'Selected size is not available for this item.'
                )

        return self.cleaned_data

    def save(self, action):

        if self.instance.discount and action in ('clear', 'remove', 'add'):
            self.instance.reset_discount()

        if action == 'clear':
            self.instance.items.clear()
            return
        elif action == 'pay':
            self.instance.pay()
            return

        item = Item.objects.get(id=self.cleaned_data['item'])
        size = self.cleaned_data['size']

        existing_relation = OrderItemRelation.objects \
            .filter(order=self.instance, item=item, size=size) \
            .first()

        if existing_relation and action == 'add':
            raise ValidationError(
                'This item with the selected size is already in your cart.'  # noqa
            )
        else:
            try:
                existing_relation.delete() \
                    if action == 'remove' \
                    else OrderItemRelation.objects \
                    .create(order=self.instance, item=item, size=size)
            except IntegrityError:
                raise ValidationError(
                    'There was an error adding the item to your cart. Please try again.'  # noqa
                )


class RecalculateCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']
        self.fields = {k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                       k.startswith(('quantity', 'item', 'size'))}

    def save(self):
        if self.instance.discount:
            self.instance.reset_discount()

        for k in self.cleaned_data.keys():
            if k.startswith('item_'):
                index = k.split('_')[-1]

                if self.cleaned_data[f'size_{index}']:
                    self.instance.items.through.objects \
                        .filter(order=self.instance,
                                item_id=self.cleaned_data[f'item_{index}'],
                                size_id=self.cleaned_data[f'size_{index}']) \
                        .update(
                            quantity=self.cleaned_data[f'quantity_{index}']
                        )
                else:
                    self.instance.items.through.objects \
                        .filter(order=self.instance,
                                item_id=self.cleaned_data[f'item_{index}']) \
                        .update(
                            quantity=self.cleaned_data[f'quantity_{index}']
                        )

        return self.instance


class ApplyDiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('code',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.order = kwargs['order']

    def clean_code(self):
        try:
            self.instance = Discount.objects.get(
                code=self.cleaned_data['code'],
                is_active=True
            )
        except Discount.DoesNotExist:
            raise ValidationError('Wrong discount code.')
        return self.cleaned_data['code']

    def apply(self):
        self.order.discount = self.instance
        self.order.save(update_fields=('discount',))
