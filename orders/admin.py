from django.contrib import admin


from orders.models import Order, Discount


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    ...
