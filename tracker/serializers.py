from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for Activity model with validation
    """
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def validate(self, data):
        """
        Custom validation for activity-specific fields
        """
        activity_type = data.get('activity_type')
        
        # Validate steps activity must have steps_count
        if activity_type == 'steps' and not data.get('steps_count'):
            raise serializers.ValidationError(
                "Steps count is required for steps activity"
            )
        
        # Validate calories is positive
        if data.get('calories') and data.get('calories') < 0:
            raise serializers.ValidationError(
                "Calories must be a positive number"
            )
        
        # Validate duration is positive
        if data.get('duration_minutes') and data.get('duration_minutes') < 0:
            raise serializers.ValidationError(
                "Duration must be a positive number"
            )
        
        return data