from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Activity
from .serializers import UserSerializer, ActivitySerializer


class RegisterView(generics.CreateAPIView):
    """
    User Registration Endpoint
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    User Login Endpoint
    POST /api/auth/login/
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    User Logout Endpoint
    POST /api/auth/logout/
    Requires: Authorization header with Token
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

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