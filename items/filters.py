import django_filters

from items.models import Item, PopularItem, Category
from shop.model_choices import Currency


class ItemFilter(django_filters.FilterSet):
    actual_price = django_filters.RangeFilter(field_name='actual_price',
                                              lookup_expr='range',
                                              label="Price")
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains',
                                     label="Name")
    currency = django_filters.ChoiceFilter(choices=Currency.choices,
                                           field_name='currency',
                                           lookup_expr='exact',
                                           label="Currency")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['category'] = django_filters.ChoiceFilter(
            choices=self.get_category_choices(),
            field_name='category',
            lookup_expr='exact',
            label="Category")

    @staticmethod
    def get_category_choices():
        return [(category.id, category.name)
                for category in Category.objects.all()]

    class Meta:
        model = Item
        fields = ['actual_price', 'name', 'category', 'currency']


class PopularItemFilter(django_filters.FilterSet):
    actual_price = django_filters.RangeFilter(
        field_name='item__actual_price',
        lookup_expr='range',
        label="Price")
    name = django_filters.CharFilter(
        field_name='item__name',
        lookup_expr='icontains',
        label="Name")
    currency = django_filters.ChoiceFilter(
        choices=Currency.choices,
        field_name='item__currency',
        lookup_expr='exact',
        label="Currency")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['item__category'] = django_filters.ChoiceFilter(
            choices=self.get_category_choices(),
            field_name='item__category',
            lookup_expr='exact',
            label="Category")

    @staticmethod
    def get_category_choices():
        return [(category.id, category.name)
                for category in Category.objects.all()]

    class Meta:
        model = PopularItem
        fields = ['actual_price', 'name', 'item__category', 'currency']
