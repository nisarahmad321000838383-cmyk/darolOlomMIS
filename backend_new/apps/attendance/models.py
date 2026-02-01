"""
Attendance models for students and teachers
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.academics.models import SchoolClass, Subject
from apps.accounts.models import User


class StudentAttendance(TimeStampedModel):
    """
    Model for tracking student attendance
    """
    STATUS_CHOICES = [
        ('present', 'حاضر'),
        ('absent', 'غایب'),
        ('late', 'تاخیر'),
        ('excused', 'مرخصی'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='دانش‌آموز'
    )
    date = models.DateField('تاریخ')
    status = models.CharField('وضعیت', max_length=20, choices=STATUS_CHOICES, default='present')
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_attendances',
        verbose_name='صنف'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_attendances',
        verbose_name='مضمون'
    )
    remarks = models.TextField('یادداشت', blank=True)
    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_student_attendances',
        verbose_name='ثبت شده توسط'
    )

    class Meta:
        verbose_name = 'حاضری دانش‌آموز'
        verbose_name_plural = 'حاضری دانش‌آموزان'
        ordering = ['-date', '-created_at']
        unique_together = ['student', 'date', 'subject']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"


class TeacherAttendance(TimeStampedModel):
    """
    Model for tracking teacher attendance
    """
    STATUS_CHOICES = [
        ('present', 'حاضر'),
        ('absent', 'غایب'),
        ('late', 'تاخیر'),
        ('leave', 'مرخصی'),
    ]

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='استاد'
    )
    date = models.DateField('تاریخ')
    status = models.CharField('وضعیت', max_length=20, choices=STATUS_CHOICES, default='present')
    check_in_time = models.TimeField('زمان ورود', null=True, blank=True)
    check_out_time = models.TimeField('زمان خروج', null=True, blank=True)
    remarks = models.TextField('یادداشت', blank=True)
    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_teacher_attendances',
        verbose_name='ثبت شده توسط'
    )

    class Meta:
        verbose_name = 'حاضری استاد'
        verbose_name_plural = 'حاضری اساتید'
        ordering = ['-date', '-created_at']
        unique_together = ['teacher', 'date']

    def __str__(self):
        return f"{self.teacher} - {self.date} - {self.get_status_display()}"
