from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Inventory, StockRequest, DistributorStockRequest


def approve_distributor_stock_request(stock_request: DistributorStockRequest):
    """
    Company → Distributor stock movement
    """

    if stock_request.status != "PENDING":
        raise ValidationError("Only pending distributor stock requests can be approved")

    company = stock_request.company
    distributor = stock_request.distributor
    product = stock_request.product
    quantity = stock_request.quantity

    if distributor.company_id != company.id:
        raise ValidationError("Distributor does not belong to this company")

    with transaction.atomic():
        try:
            company_inventory = Inventory.objects.select_for_update().get(
                product=product,
                company=company,
                distributor__isnull=True,
                store__isnull=True
            )
        except Inventory.DoesNotExist:
            raise ValidationError("Company inventory not found for this product")

        if company_inventory.quantity < quantity:
            raise ValidationError("Not enough company inventory available")

        distributor_inventory, created = Inventory.objects.get_or_create(
            product=product,
            company=None,
            distributor=distributor,
            store=None,
            defaults={"quantity": quantity}
        )

        company_inventory.quantity -= quantity
        company_inventory.save()

        if not created:
            distributor_inventory.quantity += quantity
            distributor_inventory.save()

        stock_request.status = "APPROVED"
        stock_request.save()

    return stock_request


def reject_distributor_stock_request(stock_request: DistributorStockRequest):
    if stock_request.status != "PENDING":
        raise ValidationError("Only pending distributor stock requests can be rejected")

    stock_request.status = "REJECTED"
    stock_request.save()

    return stock_request


def approve_store_stock_request(stock_request: StockRequest):
    """
    Distributor → Store stock movement
    """

    if stock_request.status != "PENDING":
        raise ValidationError("Only pending store stock requests can be approved")

    store = stock_request.store
    distributor = stock_request.distributor
    product = stock_request.product
    quantity = stock_request.quantity

    if store.distributor_id != distributor.id:
        raise ValidationError("Store does not belong to this distributor")

    with transaction.atomic():
        try:
            distributor_inventory = Inventory.objects.select_for_update().get(
                product=product,
                company__isnull=True,
                distributor=distributor,
                store__isnull=True
            )
        except Inventory.DoesNotExist:
            raise ValidationError("Distributor inventory not found for this product")

        if distributor_inventory.quantity < quantity:
            raise ValidationError("Not enough distributor inventory available")

        store_inventory, created = Inventory.objects.get_or_create(
            product=product,
            company=None,
            distributor=None,
            store=store,
            defaults={"quantity": quantity}
        )
        distributor_inventory.quantity -= quantity
        distributor_inventory.save()

        if not created:
            store_inventory.quantity += quantity
            store_inventory.save()

        stock_request.status = "APPROVED"
        stock_request.save()

    return stock_request


def reject_store_stock_request(stock_request: StockRequest):
    if stock_request.status != "PENDING":
        raise ValidationError("Only pending store stock requests can be rejected")

    stock_request.status = "REJECTED"
    stock_request.save()

    return stock_request