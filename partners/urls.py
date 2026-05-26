from django.urls import path
from .views import (
    CompanyListCreateAPIView,
    DistributorListCreateAPIView,
    StoreListCreateAPIView,
)

urlpatterns = [
    path("companies/", CompanyListCreateAPIView.as_view()),
    path("distributors/", DistributorListCreateAPIView.as_view()),
    path("stores/", StoreListCreateAPIView.as_view()),
]