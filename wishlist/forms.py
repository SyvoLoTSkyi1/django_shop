from django import forms
from django.core.exceptions import ValidationError

from items.models import Item


class UpdateWishlistForm(forms.Form):
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
