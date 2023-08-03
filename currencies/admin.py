from django.contrib import admin

from currencies.models import CurrencyHistory


@admin.register(CurrencyHistory)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    ...
