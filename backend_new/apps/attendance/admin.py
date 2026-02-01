"""
Admin configuration for attendance app
"""
from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'school_class', 'subject', 'marked_by', 'created_at']
    list_filter = ['status', 'date', 'school_class', 'subject']
    search_fields = ['student__name', 'remarks']
    ordering = ['-date', '-created_at']
    readonly_fields = ['marked_by', 'created_at', 'updated_at']


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'date', 'status', 'check_in_time', 'check_out_time', 'marked_by', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['teacher__name', 'remarks']
    ordering = ['-date', '-created_at']
    readonly_fields = ['marked_by', 'created_at', 'updated_at']
