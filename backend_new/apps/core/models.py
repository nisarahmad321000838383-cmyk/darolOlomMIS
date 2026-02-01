"""
Base models for the application
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model with created_at and updated_at fields
    """
    created_at = models.DateTimeField('ایجاد شده در', auto_now_add=True)
    updated_at = models.DateTimeField('بروزرسانی شده در', auto_now=True)

    class Meta:
        abstract = True
