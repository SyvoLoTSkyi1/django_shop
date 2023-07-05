from django.contrib.auth import urls
from django.urls import path, include

from users.views import SignUpView

urlpatterns = [
    path('', include(urls)),
    path('sign_up/', SignUpView.as_view(), name='sign_up')
]
