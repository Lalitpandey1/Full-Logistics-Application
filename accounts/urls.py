from django.urls import path
from .views import HealthCheckAPIView

urlpatterns = [
    path("test/", HealthCheckAPIView.as_view()),
]