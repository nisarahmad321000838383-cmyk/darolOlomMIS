"""
Serializers for grades app
"""
from rest_framework import serializers
from .models import StudentScore
from apps.students.serializers import StudentListSerializer
from apps.academics.serializers import SubjectListSerializer


class StudentScoreSerializer(serializers.ModelSerializer):
    """Serializer for StudentScore model"""
    student_name = serializers.CharField(source='student.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    entered_by_name = serializers.CharField(source='entered_by.name', read_only=True)
    grade_letter = serializers.CharField(read_only=True)
    is_passing = serializers.BooleanField(read_only=True)

    class Meta:
        model = StudentScore
        fields = [
            'id', 'student', 'student_name', 'subject', 'subject_name', 'score',
            'exam_type', 'exam_type_display', 'exam_date', 'remarks', 'entered_by',
            'entered_by_name', 'grade_letter', 'is_passing', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'entered_by', 'created_at', 'updated_at']


class StudentScoreCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating scores"""
    class Meta:
        model = StudentScore
        fields = ['student', 'subject', 'score', 'exam_type', 'exam_date', 'remarks']

    def validate_score(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError('نمره باید بین 0 تا 100 باشد')
        return value


class StudentReportCardSerializer(serializers.Serializer):
    """Serializer for student report card"""
    student = StudentListSerializer(read_only=True)
    scores = StudentScoreSerializer(many=True, read_only=True)
    total_scores = serializers.IntegerField(read_only=True)
    average_score = serializers.FloatField(read_only=True)
    passing_subjects = serializers.IntegerField(read_only=True)
    failing_subjects = serializers.IntegerField(read_only=True)
