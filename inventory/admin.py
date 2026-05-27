from django.contrib import admin
from .models import Inventory, StockRequest


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "company",
        "distributor",
        "store",
        "quantity",
        "updated_at",
    )

    list_filter = (
        "product",
        "company",
        "distributor",
        "store",
    )

    search_fields = (
        "product__name",
        "company__name",
        "distributor__name",
        "store__name",
    )


@admin.register(StockRequest)
class StockRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "store",
        "distributor",
        "product",
        "quantity",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "distributor",
        "store",
        "product",
    )

    search_fields = (
        "store__name",
        "distributor__name",
        "product__name",
    )