from django.urls import path

from .views import (
    InventoryListCreateAPIView,

    DistributorStockRequestListCreateAPIView,
    DistributorStockRequestApproveAPIView,
    DistributorStockRequestRejectAPIView,

    StoreStockRequestListCreateAPIView,
    StoreStockRequestApproveAPIView,
    StoreStockRequestRejectAPIView,
)


urlpatterns = [
    # Inventory
    path("inventory/",
        InventoryListCreateAPIView.as_view()
    ),

    # --------------------------------------------------
    # Flow 1:
    # Distributor → Company
    # Distributor creates stock request to Company
    # Company approves/rejects
    # --------------------------------------------------
    path("distributor-stock-requests/",
        DistributorStockRequestListCreateAPIView.as_view()
    ),
    path("distributor-stock-requests/<int:pk>/approve/",
        DistributorStockRequestApproveAPIView.as_view()
    ),
    path("distributor-stock-requests/<int:pk>/reject/",
        DistributorStockRequestRejectAPIView.as_view()
    ),

    # --------------------------------------------------
    # Flow 2:
    # Store → Distributor
    # Store creates stock request to Distributor
    # Distributor approves/rejects
    # --------------------------------------------------
    path("store-stock-requests/",
        StoreStockRequestListCreateAPIView.as_view()
    ),
    path("store-stock-requests/<int:pk>/approve/",
        StoreStockRequestApproveAPIView.as_view()
    ),
    path("store-stock-requests/<int:pk>/reject/",
        StoreStockRequestRejectAPIView.as_view()
    ),
]