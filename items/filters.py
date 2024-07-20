import django_filters

from items.models import Item, PopularItem, Category
from shop.model_choices import Currency


def get_category_choices():
    return [(category.id, category.name) for category in Category.objects.all()]


class ItemFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='price',
                                       lookup_expr='range',
                                       label="Price")
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains',
                                     label="Name")
    category = django_filters.ChoiceFilter(choices=get_category_choices(),
                                           field_name='category',
                                           lookup_expr='exact',
                                           label="Category")
    currency = django_filters.ChoiceFilter(choices=Currency.choices,
                                           field_name='currency',
                                           lookup_expr='exact',
                                           label="Currency")

    class Meta:
        model = Item
        fields = ['price', 'name', 'category', 'currency']


class PopularItemFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='item__price',
                                       lookup_expr='range',
                                       label="Price")
    name = django_filters.CharFilter(field_name='item__name',
                                     lookup_expr='icontains',
                                     label="Name")
    category = django_filters.ChoiceFilter(choices=get_category_choices(),
                                           field_name='item__category',
                                           lookup_expr='exact',
                                           label="Category")
    currency = django_filters.ChoiceFilter(choices=Currency.choices,
                                           field_name='item__currency',
                                           lookup_expr='exact',
                                           label="Currency")

    class Meta:
        model = PopularItem
        fields = ['price', 'name', 'category', 'currency']
