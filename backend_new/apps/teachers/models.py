"""
Teacher models
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import User
from apps.academics.models import SchoolClass, Subject, Semester


class Teacher(TimeStampedModel):
    """
    Model representing a teacher with extended profile information
    """
    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]
    
    EDUCATION_CHOICES = [
        ('p', 'چهارده پاس'),
        ('b', 'لیسانس'),
        ('m', 'ماستر'),
        ('d', 'دوکتور'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'role': 'TEACHER'},
        verbose_name='کاربر'
    )
    
    # Personal Information
    name = models.CharField('نام و تخلص استاد', max_length=255)
    father_name = models.CharField('نام پدر', max_length=255, blank=True)
    id_number = models.CharField('نمبر تذکره', max_length=100, blank=True)
    gender = models.CharField('جنسیت', max_length=10, choices=GENDER_CHOICES, default='male')
    
    # Address Information
    current_address = models.TextField('سکونت فعلی', blank=True)
    permanent_address = models.TextField('سکونت اصلی', blank=True)
    
    # Contact Information
    mobile_number = models.CharField('شماره موبایل', max_length=20, blank=True)
    emergency_contact = models.CharField('تماس اضطراری', max_length=20, blank=True)
    
    # Education
    education_level = models.CharField(
        'سویه تحصیلی',
        max_length=2,
        choices=EDUCATION_CHOICES,
        default='b'
    )
    specialization = models.CharField('تخصص', max_length=255, blank=True)
    
    # Academic Relations
    classes = models.ManyToManyField(
        SchoolClass,
        blank=True,
        related_name='teachers',
        verbose_name='صنوف'
    )
    subjects = models.ManyToManyField(
        Subject,
        blank=True,
        related_name='teachers',
        verbose_name='مضامین'
    )
    semesters = models.ManyToManyField(
        Semester,
        blank=True,
        related_name='teachers',
        verbose_name='سمسترها'
    )
    
    # Media
    image = models.ImageField('عکس', upload_to='teachers/', blank=True, null=True)
    
    # Additional Information
    notes = models.TextField('یادداشت‌ها', blank=True)
    is_active = models.BooleanField('فعال', default=True)
    hire_date = models.DateField('تاریخ استخدام', blank=True, null=True)

    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'اساتید'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.id_number or '—'})"

    @property
    def full_name(self):
        return f"{self.name} {self.father_name}"
