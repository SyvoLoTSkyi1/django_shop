from django.contrib import admin

from items.models import Item, Product, Category


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    list_filter = ('created_at', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
    list_display = ('name', 'price', 'sku', 'created_at',)
    list_filter = ('price',)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...