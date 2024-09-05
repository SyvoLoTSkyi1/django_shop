from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from users.views import SignUpView, LoginView, \
    SignUpConfirmEmailView, SignUpConfirmPhoneView, UserProfileView, CustomLoginView, UserProfileUpdateView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('sign-up/activation_email/',
         TemplateView.as_view(
             template_name='registration/sign_up_activation_email.html'),
             name='sign_up_activation_email'),
    path('sign_up/<uidb64>/<token>/confirm/',
         SignUpConfirmEmailView.as_view(), name='sign_up_confirm_email'),
    path('sign_up/confirm_phone/',
         SignUpConfirmPhoneView.as_view(), name='sign_up_confirm_phone'),
    path('profile/',
         UserProfileView.as_view(), name='user_profile'),
    path('profile/update/',
         UserProfileUpdateView.as_view(), name='user_profile_update'),
]
