from django.urls import path

from items.views import export_csv, ItemDetail, ImportCSVIntoItems, ItemsView

urlpatterns = [
    path('items/', ItemsView.as_view(), name='items'),
    path('items/csv/', export_csv, name='export_csv'),
    path('items/<uuid:pk>', ItemDetail.as_view(), name='item_detail'),
    path('items/import_csv/', ImportCSVIntoItems.as_view(), name='import_csv'),  # noqa
]
