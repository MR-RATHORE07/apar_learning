from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class Profile(models.Model):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Enhanced fields
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, help_text="Profile picture")
    bio = models.TextField(blank=True, null=True, max_length=500)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Social/contact
    website = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    
    # Account settings
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)
    
    # Academic/Professional info
    department = models.CharField(max_length=100, blank=True, null=True, help_text="For instructors/admin")
    specialization = models.CharField(max_length=200, blank=True, null=True, help_text="For instructors")
    education_level = models.CharField(max_length=100, blank=True, null=True, help_text="For students")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

    def is_complete(self):
        """Check if profile is complete"""
        return bool(self.avatar and self.bio and self.date_of_birth)
