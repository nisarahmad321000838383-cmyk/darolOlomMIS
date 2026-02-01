"""
Academic models for semesters, classes, and subjects
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Semester(TimeStampedModel):
    """
    Model representing a semester
    """
    number = models.PositiveSmallIntegerField('شماره سمستر', unique=True)
    name = models.CharField('نام سمستر', max_length=100, blank=True)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'سمستر'
        verbose_name_plural = 'سمسترها'
        ordering = ['number']

    def __str__(self):
        persian_digits = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
        }
        persian_number = ''.join(persian_digits.get(ch, ch) for ch in str(self.number))
        return f"سمستر {persian_number}" if not self.name else self.name


class SchoolClass(TimeStampedModel):
    """
    Model representing a school class (صنف)
    """
    name = models.CharField('نام صنف', max_length=255, unique=True)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes',
        verbose_name='سمستر'
    )
    description = models.TextField('توضیحات', blank=True)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'صنف'
        verbose_name_plural = 'صنوف'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        """Get the number of students in this class"""
        return self.students.count()


class Subject(TimeStampedModel):
    """
    Model representing an academic subject (مضمون)
    """
    name = models.CharField('نام مضمون', max_length=255)
    code = models.CharField('کد مضمون', max_length=50, unique=True, blank=True, null=True)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name='سمستر مربوطه'
    )
    credits = models.PositiveSmallIntegerField('واحد', default=3)
    description = models.TextField('توضیحات', blank=True)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'مضمون'
        verbose_name_plural = 'مضامین'
        ordering = ['semester__number', 'name']

    def __str__(self):
        return f"{self.name} (سمستر {self.semester.number})"
