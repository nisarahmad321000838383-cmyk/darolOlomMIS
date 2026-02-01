"""
Views for attendance app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Count, Q
from datetime import datetime, timedelta

from .models import StudentAttendance, TeacherAttendance
from .serializers import (
    StudentAttendanceSerializer, StudentAttendanceCreateSerializer,
    TeacherAttendanceSerializer, TeacherAttendanceCreateSerializer,
    AttendanceStatsSerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin


class StudentAttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student attendance
    """
    queryset = StudentAttendance.objects.select_related(
        'student', 'school_class', 'subject', 'marked_by'
    ).all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'date', 'status', 'school_class', 'subject']
    search_fields = ['student__name', 'remarks']
    ordering_fields = ['date', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentAttendanceCreateSerializer
        return StudentAttendanceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Students can only see their own attendance
        if user.role == 'STUDENT':
            return queryset.filter(student__user=user)
        
        # Teachers can see attendance for their classes/subjects
        if user.role == 'TEACHER':
            teacher = user.teacher_profile
            return queryset.filter(
                Q(school_class__in=teacher.classes.all()) |
                Q(subject__in=teacher.subjects.all())
            )
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(marked_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        """Get attendance for a specific student"""
        queryset = self.get_queryset().filter(student_id=student_id)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats/(?P<student_id>[^/.]+)')
    def student_stats(self, request, student_id=None):
        """Get attendance statistics for a student"""
        queryset = self.get_queryset().filter(student_id=student_id)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        stats = queryset.aggregate(
            total_days=Count('id'),
            present_days=Count('id', filter=Q(status='present')),
            absent_days=Count('id', filter=Q(status='absent')),
            late_days=Count('id', filter=Q(status='late')),
            excused_days=Count('id', filter=Q(status='excused'))
        )
        
        total = stats['total_days']
        present = stats['present_days']
        attendance_percentage = (present / total * 100) if total > 0 else 0
        
        stats['attendance_percentage'] = round(attendance_percentage, 2)
        
        serializer = AttendanceStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='bulk-mark')
    def bulk_mark(self, request):
        """Bulk mark attendance for multiple students"""
        attendances_data = request.data.get('attendances', [])
        
        if not attendances_data:
            return Response(
                {'error': 'لطفاً حاضری را وارد کنید'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_attendances = []
        errors = []
        
        for attendance_data in attendances_data:
            serializer = StudentAttendanceCreateSerializer(data=attendance_data)
            if serializer.is_valid():
                attendance = serializer.save(marked_by=request.user)
                created_attendances.append(attendance)
            else:
                errors.append({
                    'data': attendance_data,
                    'errors': serializer.errors
                })
        
        return Response({
            'created': len(created_attendances),
            'errors': len(errors),
            'created_attendances': StudentAttendanceSerializer(created_attendances, many=True).data,
            'error_details': errors
        })


class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teacher attendance
    """
    queryset = TeacherAttendance.objects.select_related('teacher', 'marked_by').all()
    serializer_class = TeacherAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['teacher', 'date', 'status']
    search_fields = ['teacher__name', 'remarks']
    ordering_fields = ['date', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeacherAttendanceCreateSerializer
        return TeacherAttendanceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Teachers can only see their own attendance
        if user.role == 'TEACHER':
            return queryset.filter(teacher__user=user)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(marked_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='teacher/(?P<teacher_id>[^/.]+)')
    def by_teacher(self, request, teacher_id=None):
        """Get attendance for a specific teacher"""
        queryset = self.get_queryset().filter(teacher_id=teacher_id)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats/(?P<teacher_id>[^/.]+)')
    def teacher_stats(self, request, teacher_id=None):
        """Get attendance statistics for a teacher"""
        queryset = self.get_queryset().filter(teacher_id=teacher_id)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        stats = queryset.aggregate(
            total_days=Count('id'),
            present_days=Count('id', filter=Q(status='present')),
            absent_days=Count('id', filter=Q(status='absent')),
            late_days=Count('id', filter=Q(status='late')),
            leave_days=Count('id', filter=Q(status='leave'))
        )
        
        total = stats['total_days']
        present = stats['present_days']
        attendance_percentage = (present / total * 100) if total > 0 else 0
        
        stats['attendance_percentage'] = round(attendance_percentage, 2)
        stats['excused_days'] = stats.pop('leave_days')  # Rename for consistency
        
        serializer = AttendanceStatsSerializer(stats)
        return Response(serializer.data)
