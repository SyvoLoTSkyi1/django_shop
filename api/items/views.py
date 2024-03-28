from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.items.serializers import ItemSerializer, CategorySerializer
from items.models import Item, Category


class ItemsViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]


class CategoriesViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='items',
            serializer_class=ItemSerializer)
    def get_items(self, request, *args, **kwargs):
        """
        /api/v1/categories/:id/items/
        :param request:
        :param pk:
        :return:
        """
        category = self.get_object()
        items = category.item_set
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
