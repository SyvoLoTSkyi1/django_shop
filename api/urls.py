from django.urls import path, include
from api.items.urls import urlpatterns as items_urlpatterns

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(items_urlpatterns)),

]
