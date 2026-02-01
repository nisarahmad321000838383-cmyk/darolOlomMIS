"""
Base permission classes
"""
from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Permission class that allows only super admin users
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'SUPER_ADMIN'
        )


class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Permission class that allows super admin and admin users
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['SUPER_ADMIN', 'ADMIN']
        )


class IsTeacher(permissions.BasePermission):
    """
    Permission class that allows only teacher users
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'TEACHER'
        )


class IsStudent(permissions.BasePermission):
    """
    Permission class that allows only student users
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'STUDENT'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class that allows owners to edit their own objects or admins
    """
    def has_object_permission(self, request, view, obj):
        # Admin and super admin can do anything
        if request.user.role in ['SUPER_ADMIN', 'ADMIN']:
            return True
        
        # Check if object has user field and it matches the request user
        return hasattr(obj, 'user') and obj.user == request.user
