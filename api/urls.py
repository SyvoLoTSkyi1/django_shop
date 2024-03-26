from django.urls import path, include
from api.items.urls import urlpatterns as items_urlpatterns
from api.feedbacks.urls import urlpatterns as feedbacks_urlpatterns

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(items_urlpatterns)),
    path('', include(feedbacks_urlpatterns)),
]
