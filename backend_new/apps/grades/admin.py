"""
Admin configuration for grades app
"""
from django.contrib import admin
from .models import StudentScore


@admin.register(StudentScore)
class StudentScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'score', 'exam_type', 'exam_date', 'entered_by', 'created_at']
    list_filter = ['exam_type', 'subject', 'exam_date']
    search_fields = ['student__name', 'subject__name']
    ordering = ['-created_at']
    readonly_fields = ['entered_by', 'created_at', 'updated_at']
