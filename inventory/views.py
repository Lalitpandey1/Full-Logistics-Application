from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Inventory, StockRequest
from .serializers import InventorySerializer, StockRequestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .services import approve_stock_request, reject_stock_request


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
    
class StockRequestApproveAPIView(APIView):
    def patch(self, request, pk):
        stock_request = get_object_or_404(StockRequest, id=pk)
        try:
            approved_request = approve_stock_request(stock_request)
        except ValidationError as error:
            return Response(
                {"error": error.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StockRequestSerializer(approved_request)

        return Response(
            {
                "message": "Stock request approved successfully",
                "stock_request": serializer.data
            },
            status=status.HTTP_200_OK
        )

class StockRequestRejectAPIView(APIView):

    def patch(self, request, pk):
        stock_request = get_object_or_404(StockRequest, id=pk)

        try:
            rejected_request = reject_stock_request(stock_request)
        except ValidationError as error:
            return Response(
                {"error": error.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StockRequestSerializer(rejected_request)

        return Response(
            {
                "message": "Stock request rejected successfully",
                "stock_request": serializer.data
            },
            status=status.HTTP_200_OK
        )