from django.contrib import admin
from .models import ProductInventory


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = [
        "product_name",
        "product_quantity",
        "product_price",
        "buy_price",
        "in_stock",
    ]
    search_fields = ["product_name"]
    list_filter = ["in_stock"]
