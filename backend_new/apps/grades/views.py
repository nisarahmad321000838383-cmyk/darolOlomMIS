"""
Views for grades app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Avg, Count, Q

from .models import StudentScore
from .serializers import StudentScoreSerializer, StudentScoreCreateSerializer, StudentReportCardSerializer
from apps.core.permissions import IsAdminOrSuperAdmin, IsTeacher


class StudentScoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student scores
    """
    queryset = StudentScore.objects.select_related('student', 'subject', 'entered_by').all()
    serializer_class = StudentScoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'subject', 'exam_type']
    search_fields = ['student__name', 'subject__name']
    ordering_fields = ['score', 'exam_date', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Teachers and admins can manage grades
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentScoreCreateSerializer
        return StudentScoreSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Students can only see their own scores
        if user.role == 'STUDENT':
            return queryset.filter(student__user=user)
        
        # Teachers can see scores for subjects they teach
        if user.role == 'TEACHER':
            teacher = user.teacher_profile
            return queryset.filter(subject__in=teacher.subjects.all())
        
        # Admins and SuperAdmins can see all scores
        return queryset

    def perform_create(self, serializer):
        serializer.save(entered_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(entered_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        """Get all scores for a specific student"""
        queryset = self.get_queryset().filter(student_id=student_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='subject/(?P<subject_id>[^/.]+)')
    def by_subject(self, request, subject_id=None):
        """Get all scores for a specific subject"""
        queryset = self.get_queryset().filter(subject_id=subject_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='report-card/(?P<student_id>[^/.]+)')
    def report_card(self, request, student_id=None):
        """Get complete report card for a student"""
        from apps.students.models import Student
        
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {'error': 'دانش‌آموز یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        scores = self.get_queryset().filter(student=student)
        
        # Calculate statistics
        total_scores = scores.count()
        average_score = scores.aggregate(Avg('score'))['score__avg'] or 0
        passing_subjects = scores.filter(score__gte=60).count()
        failing_subjects = scores.filter(score__lt=60).count()
        
        data = {
            'student': student,
            'scores': scores,
            'total_scores': total_scores,
            'average_score': round(average_score, 2),
            'passing_subjects': passing_subjects,
            'failing_subjects': failing_subjects,
        }
        
        serializer = StudentReportCardSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """Bulk create scores for multiple students"""
        scores_data = request.data.get('scores', [])
        
        if not scores_data:
            return Response(
                {'error': 'لطفاً نمرات را وارد کنید'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_scores = []
        errors = []
        
        for score_data in scores_data:
            serializer = StudentScoreCreateSerializer(data=score_data)
            if serializer.is_valid():
                score = serializer.save(entered_by=request.user)
                created_scores.append(score)
            else:
                errors.append({
                    'data': score_data,
                    'errors': serializer.errors
                })
        
        return Response({
            'created': len(created_scores),
            'errors': len(errors),
            'created_scores': StudentScoreSerializer(created_scores, many=True).data,
            'error_details': errors
        })
