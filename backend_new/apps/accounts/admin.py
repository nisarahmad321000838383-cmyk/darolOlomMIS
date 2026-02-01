"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AdminPermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'name', 'role', 'is_active', 'approval_status', 'created_at']
    list_filter = ['role', 'is_active', 'approval_status', 'gender']
    search_fields = ['username', 'name', 'father_name', 'email', 'phone_number']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('name', 'father_name', 'gender', 'email', 'phone_number', 'profile_image')}),
        ('نقش و دسترسی', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('وضعیت تایید', {'fields': ('approval_status', 'is_approved', 'approved_by', 'approved_at', 'rejection_reason')}),
        ('تاریخ‌ها', {'fields': ('created_at', 'updated_at', 'last_login')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'role'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(AdminPermission)
class AdminPermissionAdmin(admin.ModelAdmin):
    list_display = ['admin', 'permission_type', 'is_granted', 'granted_by', 'created_at']
    list_filter = ['is_granted', 'permission_type']
    search_fields = ['admin__username', 'admin__name']
    ordering = ['-created_at']
