from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    ActivityListCreateView, ActivityDetailView
)

urlpatterns = [
    # Authentication URLs
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # Activity URLs
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
]