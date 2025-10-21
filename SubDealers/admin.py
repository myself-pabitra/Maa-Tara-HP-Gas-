from django.contrib import admin
from .models import Subdealer,SubDealerSKUDiscount,Cylender_information


@admin.register(Subdealer)
class SubdealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'address']
    search_fields = ['name']

@admin.register(SubDealerSKUDiscount)
class SubDealerSKUDiscountAdmin(admin.ModelAdmin):
    list_display = ['subdealer', 'product', 'product_discount']


admin.site.register(Cylender_information)


