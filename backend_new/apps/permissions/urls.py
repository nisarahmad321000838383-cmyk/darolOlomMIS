"""
URL configuration for permissions app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermissionCheckViewSet

router = DefaultRouter()
router.register(r'check', PermissionCheckViewSet, basename='permission-check')

urlpatterns = [
    path('', include(router.urls)),
]
