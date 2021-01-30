from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "classification",
        "brand",
    )
    search_fields = (
        "name",
        "classification",
        "brand",
        "product_type",
        "vendor_name",
        "vendor_location",
    )
    list_filter = (
        "brand",
        "vendor_location",
    )
