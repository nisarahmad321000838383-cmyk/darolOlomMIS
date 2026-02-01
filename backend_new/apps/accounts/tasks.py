"""
Celery tasks for accounts app
"""
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import User


@shared_task
def cleanup_expired_pending_accounts():
    """
    Delete pending student accounts that have not been approved/rejected
    within the configured time period (default: 6 months)
    """
    expiry_months = getattr(settings, 'PENDING_ACCOUNT_EXPIRY_MONTHS', 6)
    expiry_date = timezone.now() - timedelta(days=expiry_months * 30)
    
    expired_accounts = User.objects.filter(
        role='STUDENT',
        approval_status='pending',
        created_at__lt=expiry_date
    )
    
    count = expired_accounts.count()
    expired_accounts.delete()
    
    return f"Deleted {count} expired pending accounts"
