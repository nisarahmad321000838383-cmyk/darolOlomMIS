"""
Student models
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import User
from apps.academics.models import SchoolClass, Semester


class Student(TimeStampedModel):
    """
    Model representing a student with extended profile information
    """
    GENDER_CHOICES = [
        ('male', 'مذکر'),
        ('female', 'مونث'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': 'STUDENT'},
        verbose_name='کاربر'
    )
    
    # Personal Information
    name = models.CharField('نام', max_length=255)
    father_name = models.CharField('نام پدر', max_length=255, blank=True)
    grandfather_name = models.CharField('نام پدر کلان', max_length=255, blank=True)
    id_number = models.CharField('نمبر تذکره', max_length=100, blank=True)
    exam_number = models.CharField('نمبر امتحان کانکور', max_length=100, blank=True)
    gender = models.CharField('جنسیت', max_length=10, choices=GENDER_CHOICES, default='male')
    
    # Address Information
    current_address = models.TextField('نشانی فعلی', blank=True)
    permanent_address = models.TextField('نشانی دایمی', blank=True)
    
    # Contact Information
    mobile_number = models.CharField('شماره موبایل', max_length=20, blank=True)
    emergency_contact = models.CharField('تماس اضطراری', max_length=20, blank=True)
    
    # Academic Information
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='صنف'
    )
    semesters = models.ManyToManyField(
        Semester,
        blank=True,
        related_name='students',
        verbose_name='سمسترها'
    )
    
    # Schedule Information
    time_start = models.TimeField('تایم آغاز', blank=True, null=True)
    time_end = models.TimeField('تایم ختم', blank=True, null=True)
    
    # Media
    image = models.ImageField('عکس', upload_to='students/', blank=True, null=True)
    
    # Additional Information
    notes = models.TextField('یادداشت‌ها', blank=True)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'دانش‌آموز'
        verbose_name_plural = 'دانش‌آموزان'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.father_name})"

    @property
    def full_name(self):
        return f"{self.name} {self.father_name}"
