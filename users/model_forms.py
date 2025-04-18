from django import forms
from django.conf import settings  # noqa
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.cache import cache
from django.core.exceptions import ValidationError

from users.tasks import send_verification_sms, send_confirmation_email

User = get_user_model()


class SignUpModelForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("email", "phone",)
        field_classes = {'email': UsernameField}

    def clean(self):
        cleaned_data = super().clean()
        self.instance.is_active = False
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not email and not phone:
            raise ValidationError('Email or phone number is required')
        elif not password1 or not password2:
            raise ValidationError('Enter correct password')
        elif password1 != password2:
            raise ValidationError('Password1 not equal password2')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)

        if self.cleaned_data.get("phone") \
                and not self.cleaned_data.get("email"):
            phone = self.cleaned_data.get("phone")
            send_verification_sms.delay(user.id, str(phone))
        else:
            send_confirmation_email.delay(user.id)

        return user


class ConfirmPhoneForm(forms.Form):
    code = forms.IntegerField(min_value=10000, max_value=99999)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def is_valid(self, user_id=None):
        valid = super().is_valid()

        if valid:
            cache_code = cache.get(f'{str(user_id)}_code')
            input_code = self.cleaned_data['code']
            if cache_code == input_code:
                return True
            else:
                self.add_error('code', 'Invalid code. Please try again.')
                return False

    def save(self, user_id=None):
        user = User.objects.get(id=user_id)
        if not user.is_active:
            user.is_active = True
        user.is_phone_valid = True
        user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'country', 'city', 'address', )

    def __init__(self, *args, **kwargs):
        require_fields = kwargs.pop('require_fields', False)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for field in ['email', 'phone']:
            if getattr(self.instance, f'is_{field}_valid', False):
                self.fields[field].disabled = True

        if require_fields:
            required_fields = ['first_name', 'last_name',
                               'country', 'city', 'address']
            for field in required_fields:
                self.fields[field].required = True
