from rest_framework import serializers
from .models import Inventory, StockRequest


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRequest
        fields = "__all__"