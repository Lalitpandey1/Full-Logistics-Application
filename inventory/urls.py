from django.urls import path
from .views import (
    InventoryListCreateAPIView,
    StockRequestListCreateAPIView,
)

urlpatterns = [
    path("inventory/", InventoryListCreateAPIView.as_view()),
    path("stock-requests/", StockRequestListCreateAPIView.as_view()),
]