"""
Admin configuration for documents app
"""
from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'student', 'teacher', 'is_verified', 'uploaded_by', 'created_at']
    list_filter = ['document_type', 'is_verified']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['uploaded_by', 'verified_by', 'verified_at', 'created_at', 'updated_at']
