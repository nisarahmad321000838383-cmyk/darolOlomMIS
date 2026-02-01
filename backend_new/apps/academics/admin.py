"""
Admin configuration for academics app
"""
from django.contrib import admin
from .models import Semester, SchoolClass, Subject


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'number']
    ordering = ['number']


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'semester', 'is_active', 'created_at']
    list_filter = ['semester', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'semester', 'credits', 'is_active', 'created_at']
    list_filter = ['semester', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering = ['semester__number', 'name']
