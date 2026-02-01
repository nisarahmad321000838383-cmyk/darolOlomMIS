"""
Document models for file uploads
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.accounts.models import User
import os


def document_upload_path(instance, filename):
    """Generate upload path for documents"""
    if instance.student:
        return f'documents/students/{instance.student.id}/{filename}'
    elif instance.teacher:
        return f'documents/teachers/{instance.teacher.id}/{filename}'
    else:
        return f'documents/general/{filename}'


class Document(TimeStampedModel):
    """
    Model for document uploads
    """
    DOCUMENT_TYPE_CHOICES = [
        ('certificate', 'گواهینامه'),
        ('transcript', 'نمره نامه'),
        ('id_document', 'سند شناسایی'),
        ('medical', 'سند طبی'),
        ('letter', 'نامه'),
        ('contract', 'قرارداد'),
        ('other', 'سایر'),
    ]

    title = models.CharField('عنوان', max_length=255)
    description = models.TextField('توضیحات', blank=True)
    document_type = models.CharField('نوع سند', max_length=50, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField('فایل', upload_to=document_upload_path)
    
    # Relations - document can belong to student, teacher, or be general
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name='دانش‌آموز'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name='استاد'
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name='بارگذاری شده توسط'
    )
    
    is_verified = models.BooleanField('تایید شده', default=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents',
        verbose_name='تایید شده توسط'
    )
    verified_at = models.DateTimeField('تاریخ تایید', null=True, blank=True)

    class Meta:
        verbose_name = 'سند'
        verbose_name_plural = 'اسناد'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_document_type_display()}"

    @property
    def file_name(self):
        """Get the file name from the file path"""
        return os.path.basename(self.file.name)

    @property
    def file_size(self):
        """Get file size in KB"""
        try:
            return round(self.file.size / 1024, 2)
        except:
            return 0

    @property
    def file_extension(self):
        """Get file extension"""
        return os.path.splitext(self.file.name)[1]

    def delete(self, *args, **kwargs):
        """Override delete to remove file from storage"""
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
