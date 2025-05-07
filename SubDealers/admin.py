from django.contrib import admin
from .models import Subdealer, SubdealerInventory


@admin.register(Subdealer)
class SubdealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'address', 'discount']
    search_fields = ['name']

@admin.register(SubdealerInventory)
class SubdealerInventoryAdmin(admin.ModelAdmin):
    list_display = ['subdealer', 'product', 'discounted_price']
    search_fields = ['subdealer__name', 'product__product_name']
