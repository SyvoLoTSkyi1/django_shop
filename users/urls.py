from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import SignUpView, LoginView, \
    SignUpConfirmEmailView, SignUpConfirmPhoneView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('sign_up/<uidb64>/<token>/confirm/',
         SignUpConfirmEmailView.as_view(), name='sign_up_confirm_email'),
    path('sign_up/confirmphone/',
         SignUpConfirmPhoneView.as_view(), name='sign_up_confirm_phone')
]
