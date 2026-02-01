"""
Grade models for student scores
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.students.models import Student
from apps.academics.models import Subject
from apps.accounts.models import User


class StudentScore(TimeStampedModel):
    """
    Model to store a student's score for a subject
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='دانش‌آموز'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='مضمون'
    )
    score = models.PositiveSmallIntegerField(
        'نمره',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    exam_type = models.CharField(
        'نوع امتحان',
        max_length=50,
        choices=[
            ('midterm', 'میان ترم'),
            ('final', 'فاینل'),
            ('quiz', 'کوییز'),
            ('assignment', 'تکلیف'),
        ],
        default='final'
    )
    exam_date = models.DateField('تاریخ امتحان', null=True, blank=True)
    remarks = models.TextField('یادداشت', blank=True)
    entered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entered_scores',
        verbose_name='ثبت شده توسط'
    )

    class Meta:
        verbose_name = 'نمره دانش‌آموز'
        verbose_name_plural = 'نمرات دانش‌آموزان'
        ordering = ['-created_at']
        unique_together = ['student', 'subject', 'exam_type']

    def __str__(self):
        return f"{self.student} — {self.subject}: {self.score if self.score is not None else '—'}"

    @property
    def grade_letter(self):
        """Convert numeric score to letter grade"""
        if self.score is None:
            return 'N/A'
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'

    @property
    def is_passing(self):
        """Check if score is passing (>=60)"""
        return self.score is not None and self.score >= 60
