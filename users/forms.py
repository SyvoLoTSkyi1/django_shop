from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError


# User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             required=False)
    phone = forms.CharField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        phone = self.cleaned_data.get('phone')

        if not username and not phone:
            raise ValidationError('Email or phone number is required')
        if password:
            kwargs = {'password': password}
            if phone and not username:
                kwargs.update({'phone': phone})
            else:
                kwargs.update({'username': username})
            self.user_cache = authenticate(self.request, **kwargs)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone']  # Додайте поля, які потрібно редагувати
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
#             raise forms.ValidationError('Цей email вже використовується іншим користувачем.')
#         return email
#
#     def clean_phone(self):
#         phone = self.cleaned_data.get('phone')
#         if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
#             raise forms.ValidationError('Цей phone вже використовується іншим користувачем.')
#         return phone
