from django import forms
from django.contrib.auth.models import User


class SignUpModelForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        required=True
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        required=True
    )
    password2 = forms.CharField(
        label='Password Again',
        widget=forms.PasswordInput(),
        required=True
    )
    error_massages = {'password_error': 'Passwords don`t match'}

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def is_valid(self):
        if not self.errors:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 != password2:
                self.errors.update(self.error_massages)
        return super().is_valid()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0]
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
