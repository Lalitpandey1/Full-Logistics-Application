from django.urls import path
from .views import (
    InventoryListCreateAPIView,
    StockRequestListCreateAPIView,
    StockRequestApproveAPIView,
    StockRequestRejectAPIView,
)

urlpatterns = [
    path("inventory/", InventoryListCreateAPIView.as_view()),
    path("stock-requests/", StockRequestListCreateAPIView.as_view()),
    path("stock-requests/<int:pk>/approve/", StockRequestApproveAPIView.as_view()),
    path("stock-requests/<int:pk>/reject/", StockRequestRejectAPIView.as_view()),
]