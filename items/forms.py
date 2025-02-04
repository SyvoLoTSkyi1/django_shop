import codecs
import csv

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from items.models import Item, Category


class ImportForm(forms.Form):
    csv_file = forms.FileField(validators=[FileExtensionValidator(['csv'])])

    def clean_csv_file(self):
        uploaded_file = self.cleaned_data['csv_file']
        reader = csv.DictReader(codecs.iterdecode(uploaded_file, 'utf-8'))
        items_list = []
        for row in reader:
            try:
                items_list.append(
                    Item(
                        name=row['name'],
                        description=row['description'],
                        price=row['price'],
                        sku=row['sku'],
                        category=Category.objects.get_or_create(
                            name=row['category'])[0],
                        image=row['image']
                    )
                )
            except KeyError as error:
                raise ValidationError(error)
        return items_list

    def save(self):
        Item.objects.bulk_create(self.cleaned_data['csv_file'])
