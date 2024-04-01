import django_filters

from items.models import Item


class ItemFilter(django_filters.FilterSet):

    class Meta:
        model = Item
        fields = {
            'price': ['range'],
            'name': ['icontains'],
            'category': ['exact'],
            'currency': ['exact'],
        }
