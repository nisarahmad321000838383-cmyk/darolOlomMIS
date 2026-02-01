"""
Views for permissions app - utilities for checking permissions
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.accounts.models import AdminPermission


class PermissionCheckViewSet(viewsets.ViewSet):
    """
    ViewSet for checking user permissions
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_permissions(self, request):
        """Get current user's permissions"""
        user = request.user
        
        if user.role == 'SUPER_ADMIN':
            # Super admin has all permissions
            all_permissions = [choice[0] for choice in AdminPermission.PERMISSION_CHOICES]
            return Response({
                'role': 'SUPER_ADMIN',
                'permissions': all_permissions,
                'has_all_permissions': True
            })
        
        elif user.role == 'ADMIN':
            # Get admin's granted permissions
            permissions = AdminPermission.objects.filter(
                admin=user,
                is_granted=True
            ).values_list('permission_type', flat=True)
            
            return Response({
                'role': 'ADMIN',
                'permissions': list(permissions),
                'has_all_permissions': False
            })
        
        else:
            # Students and teachers have role-based permissions
            return Response({
                'role': user.role,
                'permissions': [],
                'has_all_permissions': False
            })

    @action(detail=False, methods=['post'])
    def check_permission(self, request):
        """Check if user has a specific permission"""
        permission = request.data.get('permission')
        
        if not permission:
            return Response(
                {'error': 'نوع دسترسی الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        has_permission = False
        
        if user.role == 'SUPER_ADMIN':
            has_permission = True
        elif user.role == 'ADMIN':
            has_permission = AdminPermission.objects.filter(
                admin=user,
                permission_type=permission,
                is_granted=True
            ).exists()
        
        return Response({
            'permission': permission,
            'has_permission': has_permission
        })

    @action(detail=False, methods=['get'])
    def available_permissions(self, request):
        """Get all available permission types"""
        permissions = [
            {
                'value': choice[0],
                'label': choice[1]
            }
            for choice in AdminPermission.PERMISSION_CHOICES
        ]
        
        return Response({
            'permissions': permissions
        })
