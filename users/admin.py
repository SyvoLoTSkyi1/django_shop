from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    permissions_fieldsets = (
        (None, {
            'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups',
                       'user_permissions'),
            'classes': ('collapse',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'is_phone_valid', 'is_email_valid', 'password')}),  # noqa
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'country', 'city', 'address')}),  # noqa
        (_('Info'),
         {'fields': ('last_login', 'date_joined', 'is_active')}),
    )
    list_display = (
        'id', 'email', 'phone', 'is_active', 'is_phone_valid', 'is_staff')
    ordering = ('email',)
