"""
Views for academics app
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Semester, SchoolClass, Subject
from .serializers import (
    SemesterSerializer, SchoolClassSerializer, SchoolClassListSerializer,
    SubjectSerializer, SubjectListSerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin


class SemesterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing semesters
    """
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name', 'number']
    ordering_fields = ['number', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active semesters"""
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SchoolClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school classes
    """
    queryset = SchoolClass.objects.select_related('semester').all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['semester', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return SchoolClassListSerializer
        return SchoolClassSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active classes"""
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students in a class"""
        from apps.students.serializers import StudentListSerializer
        school_class = self.get_object()
        students = school_class.students.all()
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing subjects
    """
    queryset = Subject.objects.select_related('semester').all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['semester', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'semester__number', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return SubjectListSerializer
        return SubjectSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active subjects"""
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-semester/(?P<semester_id>[^/.]+)')
    def by_semester(self, request, semester_id=None):
        """Get subjects by semester"""
        queryset = self.get_queryset().filter(semester_id=semester_id, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
