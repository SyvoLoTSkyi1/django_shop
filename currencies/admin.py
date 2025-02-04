from django.contrib import admin

from currencies.models import CurrencyHistory


@admin.register(CurrencyHistory)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('currency', 'buy', 'sale', 'created_at')
    list_display = ('currency', 'buy', 'sale', 'created_at')
