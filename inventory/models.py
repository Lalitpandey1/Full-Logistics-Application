from django.db import models
from django.core.exceptions import ValidationError
from catalog.models import Product
from partners.models import Distributor, Store


class Inventory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inventories"
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
        if self.distributor and self.store:
            raise ValidationError("Inventory cannot belong to both distributor and store.")
        if not self.distributor and not self.store:
            raise ValidationError("Inventory must belong to either distributor or store.")

    def __str__(self):
        if self.distributor:
            return f"{self.product.name} - {self.distributor.name} - {self.quantity}"
        return f"{self.product.name} - {self.store.name} - {self.quantity}"


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