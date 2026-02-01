# Config package for Django settings
from .celery import app as celery_app

__all__ = ('celery_app',)
