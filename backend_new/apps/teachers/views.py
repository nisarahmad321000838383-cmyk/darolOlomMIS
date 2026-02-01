"""
Views for teachers app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Teacher
from .serializers import TeacherSerializer, TeacherListSerializer, TeacherCreateSerializer
from apps.core.permissions import IsAdminOrSuperAdmin, IsTeacher


class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teachers
    """
    queryset = Teacher.objects.select_related('user').prefetch_related('classes', 'subjects', 'semesters').all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'education_level', 'is_active']
    search_fields = ['name', 'father_name', 'id_number', 'mobile_number', 'specialization']
    ordering_fields = ['name', 'hire_date', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        elif self.action == 'create':
            return TeacherCreateSerializer
        return TeacherSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Teachers can only see their own profile
        if user.role == 'TEACHER':
            return queryset.filter(user=user)
        
        # Admins and SuperAdmins can see all teachers
        return queryset

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current teacher's profile"""
        if request.user.role != 'TEACHER':
            return Response(
                {'error': 'فقط اساتید می‌توانند به این بخش دسترسی داشته باشند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            teacher = Teacher.objects.get(user=request.user)
            serializer = self.get_serializer(teacher)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response(
                {'error': 'پروفایل استاد یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students taught by this teacher"""
        from apps.students.serializers import StudentListSerializer
        teacher = self.get_object()
        
        # Get students from all classes this teacher teaches
        students = set()
        for school_class in teacher.classes.all():
            students.update(school_class.students.all())
        
        serializer = StudentListSerializer(list(students), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records marked by this teacher"""
        from apps.attendance.serializers import TeacherAttendanceSerializer
        teacher = self.get_object()
        attendance = teacher.attendance_records.select_related('marked_by').all()
        serializer = TeacherAttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-subject/(?P<subject_id>[^/.]+)')
    def by_subject(self, request, subject_id=None):
        """Get teachers by subject"""
        queryset = self.get_queryset().filter(subjects__id=subject_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-class/(?P<class_id>[^/.]+)')
    def by_class(self, request, class_id=None):
        """Get teachers by class"""
        queryset = self.get_queryset().filter(classes__id=class_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
