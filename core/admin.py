from django.contrib import admin
from .models import Student, Subject


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('name', 'father_name', 'mobile_number', 'created_at')
	search_fields = ('name', 'father_name', 'mobile_number')
	list_per_page = 20


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'semester', 'created_at')
	search_fields = ('name',)
	list_filter = ('semester',)
	list_per_page = 20
