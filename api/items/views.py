from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.items.serializers import ItemSerializer, ItemRetrieveSerializer
from items.models import Item


class ItemsViewList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]


class ItemsViewRetrieve(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemRetrieveSerializer
    permission_classes = [IsAuthenticated]
