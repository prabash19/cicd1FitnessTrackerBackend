from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    Admin interface for Activity model
    """
    list_display = (
        'id',
        'user', 
        'activity_type', 
        'title', 
        'status', 
        'date', 
        'calories',
        'created_at'
    )
    list_filter = ('activity_type', 'status', 'date', 'user')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'activity_type', 'title', 'description', 'status')
        }),
        ('Measurements', {
            'fields': ('duration_minutes', 'calories', 'steps_count')
        }),
        ('Dates', {
            'fields': ('date', 'created_at', 'updated_at')
        }),
    )