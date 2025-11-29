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
class ActivityUpdateView(APIView):
    """
    Custom Activity Update Endpoint
    PUT /api/activities/{id}/update/
    PATCH /api/activities/{id}/update/
    
    Allows full update (PUT) or partial update (PATCH) of an activity
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_activity(self, activity_id, user):
        """
        Helper method to get activity and ensure it belongs to the user
        """
        return get_object_or_404(
            Activity, 
            id=activity_id, 
            user=user
        )
    
    def put(self, request, activity_id):
        """
        Full update - all fields required
        """
        activity = self.get_activity(activity_id, request.user)
        
        serializer = ActivitySerializer(
            activity, 
            data=request.data,
            partial=False  # Require all fields
        )
        
        if serializer.is_valid():
            updated_activity = serializer.save()
            
            return Response({
                'success': True,
                'message': 'Activity updated successfully',
                'data': ActivitySerializer(updated_activity).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, activity_id):
        """
        Partial update - only provided fields will be updated
        """
        activity = self.get_activity(activity_id, request.user)
        
        # Get the fields that are being updated
        updated_fields = list(request.data.keys())
        
        serializer = ActivitySerializer(
            activity, 
            data=request.data,
            partial=True  # Allow partial updates
        )
        
        if serializer.is_valid():
            updated_activity = serializer.save()
            
            return Response({
                'success': True,
                'message': f'Activity updated successfully. Fields updated: {", ".join(updated_fields)}',
                'updated_fields': updated_fields,
                'data': ActivitySerializer(updated_activity).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ActivityBulkUpdateView(APIView):
    """
    Bulk Update Multiple Activities
    POST /api/activities/bulk-update/
    
    Body format:
    {
        "updates": [
            {"id": 1, "duration": 45},
            {"id": 2, "title": "New Title"}
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        updates = request.data.get('updates', [])
        
        if not updates or not isinstance(updates, list):
            return Response({
                'success': False,
                'message': 'Please provide a list of updates'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = {
            'successful': [],
            'failed': []
        }
        
        for update_data in updates:
            activity_id = update_data.get('id')
            
            if not activity_id:
                results['failed'].append({
                    'data': update_data,
                    'error': 'Activity ID is required'
                })
                continue
            
            try:
                activity = Activity.objects.get(
                    id=activity_id, 
                    user=request.user
                )
                
                # 
                update_fields = {k: v for k, v in update_data.items() if k != 'id'}
                
                serializer = ActivitySerializer(
                    activity, 
                    data=update_fields,
                    partial=True
                )
                
                if serializer.is_valid():
                    serializer.save()
                    results['successful'].append({
                        'id': activity_id,
                        'updated_fields': list(update_fields.keys())
                    })
                else:
                    results['failed'].append({
                        'id': activity_id,
                        'errors': serializer.errors
                    })
                    
            except Activity.DoesNotExist:
                results['failed'].append({
                    'id': activity_id,
                    'error': 'Activity not found or does not belong to you'
                })
        
        status_code = status.HTTP_200_OK if results['successful'] else status.HTTP_400_BAD_REQUEST
        
        return Response({
            'success': len(results['successful']) > 0,
            'message': f"Updated {len(results['successful'])} activities, {len(results['failed'])} failed",
            'results': results
        }, status=status_code)


class ActivityStatusUpdateView(APIView):
    """
    Quick Status Update for Activity
    POST /api/activities/{id}/status/
    
    Body: {"status": "completed"} or {"is_completed": true}
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, activity_id):
        try:
            activity = Activity.objects.get(
                id=activity_id,
                user=request.user
            )
        except Activity.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Activity not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 
        new_status = request.data.get('status') or request.data.get('is_completed')
        
        if new_status is None:
            return Response({
                'success': False,
                'message': 'Please provide status or is_completed field'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 
        # 
        if hasattr(activity, 'completed'):
            activity.completed = new_status
        elif hasattr(activity, 'status'):
            activity.status = new_status
        
        activity.save()
        
        return Response({
            'success': True,
            'message': 'Activity status updated successfully',
            'data': ActivitySerializer(activity).data
        }, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    """
    Request Password Reset
    POST /api/auth/password-reset/request/
    Body: { "email": "user@example.com" }
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return success even if user doesn't exist (security best practice)
            return Response({
                'message': 'If an account exists with this email, you will receive a password reset link'
            }, status=status.HTTP_200_OK)
        
        # Generate token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link (adjust frontend URL as needed)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        
        # Send email
        try:
            send_mail(
                subject='Password Reset Request',
                message=f'Click the link below to reset your password:\n\n{reset_link}\n\nThis link will expire in 24 hours.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({
                'error': 'Failed to send email. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': 'If an account exists with this email, you will receive a password reset link'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Confirm Password Reset
    POST /api/auth/password-reset/confirm/
    Body: { 
        "uid": "encoded_user_id",
        "token": "reset_token",
        "new_password": "newpassword123"
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not all([uid, token, new_password]):
            return Response({
                'error': 'uid, token, and new_password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password length
        if len(new_password) < 8:
            return Response({
                'error': 'Password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Decode UID
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Invalid reset link'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Optionally, invalidate all existing tokens for this user
        Token.objects.filter(user=user).delete()
        
        return Response({
            'message': 'Password has been reset successfully'
        }, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    """
    Change Password for Authenticated User
    POST /api/auth/password-change/
    Body: { 
        "old_password": "currentpassword",
        "new_password": "newpassword123"
    }
    Requires: Authentication Token
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not all([old_password, new_password]):
            return Response({
                'error': 'old_password and new_password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify old password
        if not request.user.check_password(old_password):
            return Response({
                'error': 'Current password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate new password length
        if len(new_password) < 8:
            return Response({
                'error': 'New password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if new password is same as old
        if old_password == new_password:
            return Response({
                'error': 'New password must be different from current password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update token (optional - keeps user logged in)
        Token.objects.filter(user=request.user).delete()
        new_token = Token.objects.create(user=request.user)
        
        return Response({
            'message': 'Password changed successfully',
            'token': new_token.key
        }, status=status.HTTP_200_OK)