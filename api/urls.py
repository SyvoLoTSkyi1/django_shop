from django.urls import path, include
from api.items.urls import urlpatterns as items_urlpatterns
from api.feedbacks.urls import urlpatterns as feedbacks_urlpatterns
from rest_framework.authtoken import views


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(items_urlpatterns)),
    path('', include(feedbacks_urlpatterns)),
]
