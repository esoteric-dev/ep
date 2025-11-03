from django.contrib import admin
from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'department', 'is_admin', 'created_at')
    list_filter = ('is_admin', 'department', 'created_at')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
