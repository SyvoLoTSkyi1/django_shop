from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from users.views import SignUpView, \
    ConfirmEmailView, ConfirmPhoneView, \
    UserProfileView, CustomLoginView, UserProfileUpdateView, \
    UserOrdersView, ConfirmPhoneEmailProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('activation/email/',
         TemplateView.as_view(
             template_name='users/registration/activation_email.html'),
             name='activation_email'),
    path('email/<uidb64>/<token>/confirm/',
         ConfirmEmailView.as_view(), name='confirm_email'),
    path('phone/confirm/',
         ConfirmPhoneView.as_view(), name='confirm_phone'),
    path('profile/',
         UserProfileView.as_view(), name='user_profile'),
    path('profile/update/',
         UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('profile/orders/',
         UserOrdersView.as_view(), name='user_orders'),
    path('profile/confirm/<str:type>/',
         ConfirmPhoneEmailProfileView.as_view(),
         name='confirm_phone_email_profile'),
]
