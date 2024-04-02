from django_filters import rest_framework as filters

from items.models import Item


class ItemFilter(filters.FilterSet):

    class Meta:
        model = Item
        fields = {
            'price': ['range'],
            'name': ['icontains'],
            'category': ['exact'],
            'currency': ['exact'],
        }
