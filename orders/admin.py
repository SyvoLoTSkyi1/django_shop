from django.contrib import admin


from orders.models import Order, Discount, OrderItemRelation


class OrderItemRelationInline(admin.TabularInline):
    model = OrderItemRelation
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'discount')
    inlines = (OrderItemRelationInline,)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_filter = ('discount_type', 'is_active')
