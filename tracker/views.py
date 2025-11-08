from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Activity
from .serializers import UserSerializer, ActivitySerializer

# ... (keep existing RegisterView, LoginView, LogoutView) ...

class ActivityListCreateView(generics.ListCreateAPIView):
    """
    GET /api/activities/ - List all activities for logged-in user
    POST /api/activities/ - Create new activity
    """
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only activities for the current user
        """
        return Activity.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically set the user when creating activity
        """
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """
        Custom list response with additional info
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/activities/{id}/ - Retrieve single activity
    PUT/PATCH /api/activities/{id}/ - Update activity
    DELETE /api/activities/{id}/ - Delete activity
    """
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Ensure users can only access their own activities
        """
        return Activity.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """
        Update activity with custom response
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'data': serializer.data,
            'message': 'Activity updated successfully'
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete activity with confirmation message
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Activity deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)