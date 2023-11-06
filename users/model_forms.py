import random

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from shop.helpers import send_html_mail
from users.tasks import send_sms

User = get_user_model()


# class SignUpModelForm(forms.ModelForm):
#     email = forms.EmailField(
#         label='Email',
#         widget=forms.EmailInput(),
#         required=True
#     )
#     phone = PhoneNumberField(
#         label='Phone',
#         required=True
#     )
#     password1 = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput(),
#         required=True
#     )
#     password2 = forms.CharField(
#         label='Password Again',
#         widget=forms.PasswordInput(),
#         required=True
#     )
#     error_massages = {'password_error': 'Passwords don`t match'}
#
#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'phone', 'password1', 'password2',)
#
#     def is_valid(self):
#         if not self.errors:
#             password1 = self.cleaned_data['password1']
#             password2 = self.cleaned_data['password2']
#             if password1 != password2:
#                 self.errors.update(self.error_massages)
#         return super().is_valid()
#
#     def clean(self):
#         password1 = self.cleaned_data['password1']
#         password2 = self.cleaned_data['password2']
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords didn't match")
#         self.instance.is_active = False
#         return self.cleaned_data
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = self.cleaned_data['email'].split('@')[0]
#         user.set_password(self.cleaned_data['password1'])
#         user.is_phone_valid = True
#         context = {
#             'email': user.email,
#             'domain': settings.DOMAIN,
#             'site_name': 'SHOP',
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'user': user,
#             'token': default_token_generator.make_token(user),
#             'subject': 'Sign up confirm'
#         }
#         subject_template_name = 'registration/sign_up_confirm_subject.txt'
#         email_template_name = 'registration/sign_up_confirm_email.html'
#         send_html_mail(
#             subject_template_name,
#             email_template_name,
#             from_email=settings.SERVER_EMAIL,
#             to_email=user.email,
#             context=context
#
#         )
#         if commit:
#             user.save()
#         return user


class SignUpModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone",)
        field_classes = {'email': UsernameField}

    def clean(self):
        self.instance.is_active = False
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)

        if self.cleaned_data.get("phone") and not self.cleaned_data.get("email"):
            code = random.randint(10000, 99999)
            cache.set(f'{str(user.id)}_code', code, timeout=60)
            send_sms.delay(self.cleaned_data.get("phone"), code)

            return user

        context = {
            'email': user.email,
            'domain': settings.DOMAIN,
            'site_name': 'SHOP',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'subject': 'Confirm registration'
        }
        subject_template_name = 'registration/sign_up_confirm_subject.txt'  # noqa
        email_template_name = 'registration/sign_up_confirm_email.html'  # noqa
        send_html_mail(
            subject_template_name,
            email_template_name,
            from_email=settings.SERVER_EMAIL,
            to_email=user.email,
            context=context
        )

        return user


class SignUpConfirmPhoneForm(forms.Form):
    code = forms.CharField(min_length=5, max_length=5)

    def is_valid(self, session_user_id=None):
        if not self.errors:
            cache_code = cache.get(f'{str(session_user_id)}_code')
            input_code = self.cleaned_data['code']
            if cache_code == input_code:
                return True
            else:
                self.errors.update({'code error': 'Please, write valid code'})
                return False

    def save(self, session_user_id=None):
        user = User.objects.get(id=session_user_id)
        user.is_active = True
        user.is_phone_valid = True
        return user.save()
