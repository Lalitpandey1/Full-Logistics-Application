from django.contrib import admin
from .models import Company, Distributor, Store


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created_at")
    search_fields = ("name", "created_by__username")


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "company", "manager", "created_at")
    list_filter = ("company",)
    search_fields = ("name", "company__name", "manager__username")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "distributor", "manager", "created_at")
    list_filter = ("distributor",)
    search_fields = ("name", "distributor__name", "manager__username")