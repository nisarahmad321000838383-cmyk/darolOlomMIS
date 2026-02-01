"""
Views for students app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Student
from .serializers import StudentSerializer, StudentListSerializer, StudentCreateSerializer
from apps.core.permissions import IsAdminOrSuperAdmin, IsStudent


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing students
    """
    queryset = Student.objects.select_related('user', 'school_class').prefetch_related('semesters').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school_class', 'gender', 'is_active']
    search_fields = ['name', 'father_name', 'id_number', 'exam_number', 'mobile_number']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        elif self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Students can only see their own profile
        if user.role == 'STUDENT':
            return queryset.filter(user=user)
        
        # Teachers can see all students
        # Admins and SuperAdmins can see all students
        return queryset

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current student's profile"""
        if request.user.role != 'STUDENT':
            return Response(
                {'error': 'فقط دانش‌آموزان می‌توانند به این بخش دسترسی داشته باشند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            student = Student.objects.get(user=request.user)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {'error': 'پروفایل دانش‌آموز یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        """Get all grades for a student"""
        from apps.grades.serializers import StudentScoreSerializer
        student = self.get_object()
        scores = student.scores.select_related('subject').all()
        serializer = StudentScoreSerializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a student"""
        from apps.attendance.serializers import StudentAttendanceSerializer
        student = self.get_object()
        attendance = student.attendance_records.select_related('marked_by').all()
        serializer = StudentAttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Get documents for a student"""
        from apps.documents.serializers import DocumentSerializer
        student = self.get_object()
        documents = student.documents.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-class/(?P<class_id>[^/.]+)')
    def by_class(self, request, class_id=None):
        """Get students by class"""
        queryset = self.get_queryset().filter(school_class_id=class_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
