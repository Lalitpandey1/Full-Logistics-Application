from django.db import models
from django.core.exceptions import ValidationError

from catalog.models import Product
from partners.models import Company, Distributor, Store


class Inventory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inventories"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="inventories",
        null=True,
        blank=True
    )

    distributor = models.ForeignKey(
        Distributor,
        on_delete=models.CASCADE,
        related_name="inventories",
        null=True,
        blank=True
    )

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="inventories",
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        locations = [self.company, self.distributor, self.store]
        selected_locations = [location for location in locations if location]

        if len(selected_locations) != 1:
            raise ValidationError(
                "Inventory must belong to exactly one location: company, distributor, or store."
            )

    def __str__(self):
        if self.company:
            return f"{self.product.name} at {self.company.name}: {self.quantity}"

        if self.distributor:
            return f"{self.product.name} at {self.distributor.name}: {self.quantity}"

        return f"{self.product.name} at {self.store.name}: {self.quantity}"


class DistributorStockRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="distributor_stock_requests"
    )

    distributor = models.ForeignKey(
        Distributor,
        on_delete=models.CASCADE,
        related_name="company_stock_requests"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="distributor_stock_requests"
    )

    quantity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.distributor.name} requested {self.quantity} {self.product.name} from {self.company.name}"


class StockRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="stock_requests"
    )

    distributor = models.ForeignKey(
        Distributor,
        on_delete=models.CASCADE,
        related_name="stock_requests"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_requests"
    )

    quantity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store.name} requested {self.quantity} {self.product.name}"