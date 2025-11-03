from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TeacherProfile(models.Model):
    """Teacher profile extending Django User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacherprofile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)  # For admin privileges
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"
    
    def clean(self):
        if self.is_admin and not self.user.is_superuser:
            raise ValidationError("Admin teachers must have superuser status")
    
    class Meta:
        verbose_name = "Teacher Profile"
        verbose_name_plural = "Teacher Profiles"
