from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'email', 'is_email_verified', 'created_at']
    list_filter = ['role', 'is_email_verified', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Personal Information', {
            'fields': ('avatar', 'bio', 'phone_number', 'date_of_birth')
        }),
        ('Professional Information', {
            'fields': ('department', 'specialization', 'education_level')
        }),
        ('Social & Web', {
            'fields': ('website', 'linkedin_profile', 'github_profile'),
            'classes': ('collapse',)
        }),
        ('Account Settings', {
            'fields': ('is_email_verified', 'two_factor_enabled'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['user']
        return self.readonly_fields
