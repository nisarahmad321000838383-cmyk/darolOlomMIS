"""
Admin configuration for students app
"""
from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'father_name', 'school_class', 'gender', 'is_active', 'created_at']
    list_filter = ['school_class', 'gender', 'is_active']
    search_fields = ['name', 'father_name', 'id_number', 'exam_number', 'mobile_number']
    ordering = ['-created_at']
    filter_horizontal = ['semesters']
