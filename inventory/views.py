from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Inventory, StockRequest, DistributorStockRequest
from .serializers import (
    InventorySerializer,
    StockRequestSerializer,
    DistributorStockRequestSerializer,
)
from accounts.permissions import (
    IsCompanyAdmin,
    IsDistributorManager,
    IsStoreManager,
)
from .services import (
    approve_store_stock_request,
    reject_store_stock_request,
    approve_distributor_stock_request,
    reject_distributor_stock_request,
)


# --------------------------------------------------
# Generic Inventory API
# Inventory can belong to:
# Company OR Distributor OR Store
# --------------------------------------------------
class InventoryListCreateAPIView(APIView):
    # For now distributor manager can manage inventory.
    # Later we can refine this with object-level permissions.
    permission_classes = [IsDistributorManager]

    def get(self, request):
        inventories = Inventory.objects.all()
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------
# Flow 1:
# Distributor → Company
# Distributor requests stock from Company
# --------------------------------------------------
class DistributorStockRequestListCreateAPIView(APIView):
    permission_classes = [IsDistributorManager]

    def get(self, request):
        stock_requests = DistributorStockRequest.objects.all()
        serializer = DistributorStockRequestSerializer(stock_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DistributorStockRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------
# Flow 1 Approval:
# Company approves Distributor request
# Company inventory decreases
# Distributor inventory increases
# --------------------------------------------------
class DistributorStockRequestApproveAPIView(APIView):
    permission_classes = [IsCompanyAdmin]

    def patch(self, request, pk):
        stock_request = get_object_or_404(DistributorStockRequest, id=pk)

        try:
            approved_request = approve_distributor_stock_request(stock_request)
        except ValidationError as error:
            return Response(
                {"error": error.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DistributorStockRequestSerializer(approved_request)

        return Response(
            {
                "message": "Distributor stock request approved successfully",
                "stock_request": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# --------------------------------------------------
# Flow 1 Rejection:
# Company rejects Distributor request
# No inventory movement
# --------------------------------------------------
class DistributorStockRequestRejectAPIView(APIView):
    permission_classes = [IsCompanyAdmin]

    def patch(self, request, pk):
        stock_request = get_object_or_404(DistributorStockRequest, id=pk)

        try:
            rejected_request = reject_distributor_stock_request(stock_request)
        except ValidationError as error:
            return Response(
                {"error": error.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DistributorStockRequestSerializer(rejected_request)

        return Response(
            {
                "message": "Distributor stock request rejected successfully",
                "stock_request": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# --------------------------------------------------
# Flow 2:
# Store → Distributor
# Store requests stock from Distributor
# Model name is still StockRequest
# View name is StoreStockRequest for clarity
# --------------------------------------------------
class StoreStockRequestListCreateAPIView(APIView):
    permission_classes = [IsStoreManager]

    def get(self, request):
        stock_requests = StockRequest.objects.all()
        serializer = StockRequestSerializer(stock_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StockRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------
# Flow 2 Approval:
# Distributor approves Store request
# Distributor inventory decreases
# Store inventory increases
# --------------------------------------------------
class StoreStockRequestApproveAPIView(APIView):
    permission_classes = [IsDistributorManager]

    def patch(self, request, pk):
        stock_request = get_object_or_404(StockRequest, id=pk)

        try:
            approved_request = approve_store_stock_request(stock_request)
        except ValidationError as error:
            return Response(
                {"error": error.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StockRequestSerializer(approved_request)

        return Response(
            {
                "message": "Store stock request approved successfully",
                "stock_request": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# --------------------------------------------------
# Flow 2 Rejection:
# Distributor rejects Store request
# No inventory movement
# --------------------------------------------------
class StoreStockRequestRejectAPIView(APIView):
    permission_classes = [IsDistributorManager]

    def patch(self, request, pk):
        stock_request = get_object_or_404(StockRequest, id=pk)

        try:
            rejected_request = reject_store_stock_request(stock_request)
        except ValidationError as error:
            return Response(
                {"error": error.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StockRequestSerializer(rejected_request)

        return Response(
            {
                "message": "Store stock request rejected successfully",
                "stock_request": serializer.data,
            },
            status=status.HTTP_200_OK
        )