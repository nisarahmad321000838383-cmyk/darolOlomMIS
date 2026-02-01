"""
Views for accounts app
"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models import Q

from .models import User, AdminPermission
from .serializers import (
    UserSerializer, UserCreateSerializer, StudentRegistrationSerializer,
    LoginSerializer, UserApprovalSerializer, AdminPermissionSerializer,
    ChangePasswordSerializer, ProfileUpdateSerializer
)
from apps.core.permissions import IsSuperAdmin, IsAdminOrSuperAdmin


class AuthViewSet(viewsets.GenericViewSet):
    """
    ViewSet for authentication operations
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'], url_path='register/student')
    def register_student(self, request):
        """Student self-registration endpoint"""
        serializer = StudentRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'ثبت نام شما با موفقیت انجام شد. لطفا منتظر تایید مدیر باشید.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login endpoint"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """User logout endpoint"""
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'با موفقیت خارج شدید'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': 'رمز عبور با موفقیت تغییر یافت'})


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users (SuperAdmin and Admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    filterset_fields = ['role', 'approval_status', 'is_active', 'gender']
    search_fields = ['username', 'name', 'father_name', 'email', 'phone_number']
    ordering_fields = ['created_at', 'name', 'username']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        # Only SuperAdmin can create admins
        if self.action == 'create':
            if self.request.data.get('role') in ['ADMIN', 'SUPER_ADMIN']:
                return [IsAuthenticated(), IsSuperAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter based on user role
        user = self.request.user
        if user.is_super_admin:
            return queryset
        elif user.is_admin:
            # Admins cannot see other admins or super admins
            return queryset.exclude(role__in=['ADMIN', 'SUPER_ADMIN'])
        
        return queryset.none()

    @action(detail=False, methods=['get'], url_path='pending-students')
    def pending_students(self, request):
        """Get list of pending student registrations"""
        queryset = self.get_queryset().filter(
            role='STUDENT',
            approval_status='pending'
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='approve-reject')
    def approve_reject(self, request, pk=None):
        """Approve or reject a user (student)"""
        user = self.get_object()
        serializer = UserApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action_type = serializer.validated_data['action']
        
        if action_type == 'approve':
            user.approval_status = 'approved'
            user.is_approved = True
            user.approved_by = request.user
            user.approved_at = timezone.now()
            user.rejection_reason = ''
            message = 'کاربر با موفقیت تایید شد'
        else:
            user.approval_status = 'rejected'
            user.is_approved = False
            user.rejection_reason = serializer.validated_data.get('rejection_reason', '')
            message = 'کاربر رد شد'
        
        user.save()
        return Response({
            'message': message,
            'user': UserSerializer(user).data
        })

    @action(detail=True, methods=['post'], url_path='toggle-active')
    def toggle_active(self, request, pk=None):
        """Toggle user active status"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            'message': f'کاربر {"فعال" if user.is_active else "غیرفعال"} شد',
            'user': UserSerializer(user).data
        })


class AdminPermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing admin permissions (SuperAdmin only)
    """
    queryset = AdminPermission.objects.all()
    serializer_class = AdminPermissionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['admin', 'permission_type', 'is_granted']

    def perform_create(self, serializer):
        serializer.save(granted_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(granted_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='admin/(?P<admin_id>[^/.]+)')
    def by_admin(self, request, admin_id=None):
        """Get all permissions for a specific admin"""
        queryset = self.get_queryset().filter(admin_id=admin_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='bulk-update')
    def bulk_update(self, request):
        """Bulk update permissions for an admin"""
        admin_id = request.data.get('admin_id')
        permissions = request.data.get('permissions', [])
        
        if not admin_id:
            return Response(
                {'error': 'admin_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            admin = User.objects.get(id=admin_id, role='ADMIN')
        except User.DoesNotExist:
            return Response(
                {'error': 'Admin not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update or create permissions
        updated_permissions = []
        for perm in permissions:
            permission, created = AdminPermission.objects.update_or_create(
                admin=admin,
                permission_type=perm['permission_type'],
                defaults={
                    'is_granted': perm['is_granted'],
                    'granted_by': request.user
                }
            )
            updated_permissions.append(permission)
        
        serializer = self.get_serializer(updated_permissions, many=True)
        return Response(serializer.data)
