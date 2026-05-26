from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "company", "price", "is_active", "created_at")
    list_filter = ("company", "is_active")
    search_fields = ("name", "company__name")

    