from django import forms
from django.core.exceptions import ValidationError

from items.models import Item
from orders.models import Discount


class UpdateCartOrderForm(forms.Form):
    item = forms.UUIDField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']

    def clean(self):
        item_id = self.cleaned_data.get('item')
        if item_id:
            try:
                Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                raise ValidationError('Wrong item id.')
        return self.cleaned_data

    def save(self, action):
        if self.instance.discount and action in ('clear', 'remove', 'add',):
            self.instance.reset_discount()

        if action == 'clear':
            self.instance.items.clear()
            return
        elif action == 'pay':
            self.instance.pay()
            return
        getattr(self.instance.items, action)(self.cleaned_data['item'])


class RecalculateCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']
        self.fields = {k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                       k.startswith(('quantity', 'item'))}

    def save(self):
        if self.instance.discount:
            self.instance.reset_discount()

        for k in self.cleaned_data.keys():
            if k.startswith('item_'):
                index = k.split('_')[-1]
                self.instance.items.through.objects \
                    .filter(order=self.instance,
                            item_id=self.cleaned_data[f'item_{index}']) \
                    .update(quantity=self.cleaned_data[f'quantity_{index}'])
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
