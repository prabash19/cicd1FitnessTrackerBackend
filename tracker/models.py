from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Activity(models.Model):
    """
    Activity model for tracking workouts, meals, and steps
    """
    ACTIVITY_TYPES = [
        ('workout', 'Workout'),
        ('meal', 'Meal'),
        ('steps', 'Steps'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    # Relationships
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='activities',
        help_text="User who owns this activity"
    )
    
    # Activity details
    activity_type = models.CharField(
        max_length=20, 
        choices=ACTIVITY_TYPES,
        help_text="Type of activity"
    )
    title = models.CharField(
        max_length=200,
        help_text="Activity title"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Detailed description"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='planned',
        help_text="Current status of activity"
    )
    
    # Activity-specific measurements
    duration_minutes = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Duration in minutes (for workouts/meals)"
    )
    calories = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Calories burned/consumed"
    )
    steps_count = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Number of steps (for steps activity)"
    )
    
    # Timestamps
    date = models.DateField(
        default=timezone.now,
        help_text="Date of activity"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Activities'
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.title}"