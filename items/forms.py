import codecs
import csv

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from items.models import Item, Category
from shop.model_choices import Currency


# class ItemForm(forms.Form):
#     name = forms.CharField()
#     description = forms.CharField(required=False)
#     image = forms.ImageField()
#     category = forms.CharField()
#
#     def is_valid(self):
#         """
#         Validate data
#         :return:
#         """
#         is_valid = super().is_valid()
#         if is_valid:
#             category_name = self.cleaned_data['category']
#             try:
#                 category = Category.objects.get(name=category_name)
#             except Category.DoesNotExist:
#                 self.errors.update(
#                     {'category': f'Category {category_name} does not exist.'}
#                 )
#             else:
#                 self.cleaned_data['category'] = category
#         return is_valid
#
#     def save(self):
#         """
#         Create Item instance in database
#         :return:
#         """
#         return Item.objects.create(**self.cleaned_data)


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
                            name=row['name'])[0]
                    )
                )
            except KeyError as error:
                raise ValidationError(error)
        return items_list

    def save(self):
        Item.objects.bulk_create(self.cleaned_data['csv_file'])


class ItemFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label="Select"
    )
    currency = forms.ChoiceField(
        required=False,
        choices=[('', 'Select')] + Currency.choices,
    )

