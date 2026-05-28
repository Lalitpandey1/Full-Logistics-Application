from rest_framework import serializers
from .models import Inventory, StockRequest, DistributorStockRequest


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"

    def validate(self, data):
        company = data.get("company")
        distributor = data.get("distributor")
        store = data.get("store")

        selected = [value for value in [company, distributor, store] if value]

        if len(selected) != 1:
            raise serializers.ValidationError(
                "Inventory must belong to exactly one location: company, distributor, or store."
            )

        return data


class DistributorStockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributorStockRequest
        fields = "__all__"

    def validate(self, data):
        company = data.get("company")
        distributor = data.get("distributor")

        if distributor.company_id != company.id:
            raise serializers.ValidationError(
                "Distributor does not belong to this company."
            )

        return data


class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRequest
        fields = "__all__"

    def validate(self, data):
        store = data.get("store")
        distributor = data.get("distributor")

        if store.distributor_id != distributor.id:
            raise serializers.ValidationError(
                "Store does not belong to this distributor."
            )

        return data