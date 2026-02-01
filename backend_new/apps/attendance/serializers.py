"""
Serializers for attendance app
"""
from rest_framework import serializers
from .models import StudentAttendance, TeacherAttendance


class StudentAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for StudentAttendance model"""
    student_name = serializers.CharField(source='student.name', read_only=True)
    class_name = serializers.CharField(source='school_class.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = StudentAttendance
        fields = [
            'id', 'student', 'student_name', 'date', 'status', 'status_display',
            'school_class', 'class_name', 'subject', 'subject_name', 'remarks',
            'marked_by', 'marked_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'marked_by', 'created_at', 'updated_at']


class StudentAttendanceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating student attendance"""
    class Meta:
        model = StudentAttendance
        fields = ['student', 'date', 'status', 'school_class', 'subject', 'remarks']


class TeacherAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for TeacherAttendance model"""
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = TeacherAttendance
        fields = [
            'id', 'teacher', 'teacher_name', 'date', 'status', 'status_display',
            'check_in_time', 'check_out_time', 'remarks', 'marked_by',
            'marked_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'marked_by', 'created_at', 'updated_at']


class TeacherAttendanceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating teacher attendance"""
    class Meta:
        model = TeacherAttendance
        fields = ['teacher', 'date', 'status', 'check_in_time', 'check_out_time', 'remarks']


class AttendanceStatsSerializer(serializers.Serializer):
    """Serializer for attendance statistics"""
    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    excused_days = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
