"""
Serializers for academics app
"""
from rest_framework import serializers
from .models import Semester, SchoolClass, Subject


class SemesterSerializer(serializers.ModelSerializer):
    """Serializer for Semester model"""
    class_count = serializers.IntegerField(source='classes.count', read_only=True)
    subject_count = serializers.IntegerField(source='subjects.count', read_only=True)

    class Meta:
        model = Semester
        fields = [
            'id', 'number', 'name', 'is_active', 'class_count', 
            'subject_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SchoolClassSerializer(serializers.ModelSerializer):
    """Serializer for SchoolClass model"""
    semester_display = serializers.StringRelatedField(source='semester', read_only=True)
    student_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SchoolClass
        fields = [
            'id', 'name', 'semester', 'semester_display', 'description',
            'is_active', 'student_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SchoolClassListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing classes"""
    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'semester']


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    semester_display = serializers.StringRelatedField(source='semester', read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'code', 'semester', 'semester_display',
            'credits', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing subjects"""
    class Meta:
        model = Subject
        fields = ['id', 'name', 'semester', 'credits']
