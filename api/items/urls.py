from django.urls import path, include

from api.items.views import ItemsViewList, ItemsViewRetrieve

urlpatterns = [
    path('items/', ItemsViewList.as_view()),
    path('items/<uuid:pk>/', ItemsViewRetrieve.as_view())
]
