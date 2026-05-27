from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Inventory, StockRequest


def approve_stock_request(stock_request: StockRequest):
    if stock_request.status != "PENDING":
        raise ValidationError("Only pending stock requests can be approved")

    store = stock_request.store
    distributor = stock_request.distributor
    product = stock_request.product
    quantity = stock_request.quantity

    # Store must belong to same distributor
    if store.distributor_id != distributor.id:
        raise ValidationError("Store does not belong to this distributor")

    with transaction.atomic():
        # Find distributor inventory
        try:
            distributor_inventory = Inventory.objects.get(
                product=product,
                distributor=distributor,
                company__isnull=True,
                store__isnull=True
            )
        except Inventory.DoesNotExist:
            raise ValidationError("Distributor inventory not found for this product")

        if distributor_inventory.quantity < quantity:
            raise ValidationError("Not enough distributor inventory available")

        # Get or create store inventory
        store_inventory, created = Inventory.objects.get_or_create(
            product=product,
            store=store,
            company=None,
            distributor=None,
            defaults={"quantity": 0}
        )

        # Move stock
        distributor_inventory.quantity -= quantity
        store_inventory.quantity += quantity

        distributor_inventory.save()
        store_inventory.save()

        stock_request.status = "APPROVED"
        stock_request.save()

    return stock_request


def reject_stock_request(stock_request: StockRequest):
    if stock_request.status != "PENDING":
        raise ValidationError("Only pending stock requests can be rejected")

    stock_request.status = "REJECTED"
    stock_request.save()

    return stock_request