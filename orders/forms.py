from django import forms
from django.core.exceptions import ValidationError

from items.models import Item


class UpdateCartOrderForm(forms.Form):
    item = forms.UUIDField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']

    def clean_item_id(self):
        try:
            item = Item.objects.get(id=self.cleaned_data['item'])
        except Item.DoesNotExist:
            raise ValidationError('Wrong item id.')

        return item

    def save(self, action):
        getattr(self.instance.items, action)(self.cleaned_data['item'])


class RecalculateCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']
        self.fields = {k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                       k != 'csrfmiddlewaretoken'}

    def save(self):
        for k, v in self.cleaned_data.items():
            if k.startswith('item_'):
                index = k.split('_')[-1]
                self.instance.items.through.objects\
                    .filter(item_id=v)\
                    .update(quantity=self.cleaned_data[f'quantity_{index}'])

        return self.instance
