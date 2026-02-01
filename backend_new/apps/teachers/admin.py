"""
Admin configuration for teachers app
"""
from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'father_name', 'education_level', 'gender', 'is_active', 'created_at']
    list_filter = ['education_level', 'gender', 'is_active']
    search_fields = ['name', 'father_name', 'id_number', 'mobile_number', 'specialization']
    ordering = ['-created_at']
    filter_horizontal = ['classes', 'subjects', 'semesters']
