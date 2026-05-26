from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Inventory, StockRequest
from .serializers import InventorySerializer, StockRequestSerializer


class InventoryListCreateAPIView(APIView):

    def get(self, request):
        inventories = Inventory.objects.all()
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StockRequestListCreateAPIView(APIView):

    def get(self, request):
        stock_requests = StockRequest.objects.all()
        serializer = StockRequestSerializer(stock_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StockRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)