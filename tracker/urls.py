from django.urls import path
from .views import api_health_check, update_status

urlpatterns = [
    path("health/", api_health_check, name="api-health"),
    path("update-status/", update_status, name="update-status"),
]
