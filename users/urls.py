from django.contrib.auth import urls
from django.urls import path, include

urlpatterns = [
    path('', include(urls))
]
