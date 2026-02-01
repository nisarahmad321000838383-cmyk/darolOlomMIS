"""
Views for documents app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone

from .models import Document
from .serializers import DocumentSerializer, DocumentCreateSerializer, DocumentVerifySerializer
from apps.core.permissions import IsAdminOrSuperAdmin


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing documents
    """
    queryset = Document.objects.select_related('student', 'teacher', 'uploaded_by', 'verified_by').all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['document_type', 'student', 'teacher', 'is_verified']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DocumentCreateSerializer
        return DocumentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Students can only see their own documents
        if user.role == 'STUDENT':
            return queryset.filter(student__user=user)
        
        # Teachers can see their own documents and their students' documents
        if user.role == 'TEACHER':
            teacher = user.teacher_profile
            # Get students from teacher's classes
            student_ids = set()
            for school_class in teacher.classes.all():
                student_ids.update(school_class.students.values_list('id', flat=True))
            
            return queryset.filter(
                models.Q(teacher__user=user) |
                models.Q(student_id__in=student_ids)
            )
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        """Get all documents for a specific student"""
        queryset = self.get_queryset().filter(student_id=student_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='teacher/(?P<teacher_id>[^/.]+)')
    def by_teacher(self, request, teacher_id=None):
        """Get all documents for a specific teacher"""
        queryset = self.get_queryset().filter(teacher_id=teacher_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrSuperAdmin])
    def verify(self, request, pk=None):
        """Verify a document"""
        document = self.get_object()
        serializer = DocumentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        is_verified = serializer.validated_data['is_verified']
        document.is_verified = is_verified
        
        if is_verified:
            document.verified_by = request.user
            document.verified_at = timezone.now()
        else:
            document.verified_by = None
            document.verified_at = None
        
        document.save()
        
        return Response({
            'message': 'سند تایید شد' if is_verified else 'تایید سند لغو شد',
            'document': DocumentSerializer(document, context={'request': request}).data
        })

    @action(detail=False, methods=['get'])
    def unverified(self, request):
        """Get all unverified documents"""
        queryset = self.get_queryset().filter(is_verified=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


from django.db import models
