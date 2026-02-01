"""
URL configuration for teachers app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet

router = DefaultRouter()
router.register(r'', TeacherViewSet, basename='teachers')

urlpatterns = [
    path('', include(router.urls)),
]
