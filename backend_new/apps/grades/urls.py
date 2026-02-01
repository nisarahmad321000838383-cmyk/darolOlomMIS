"""
URL configuration for grades app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentScoreViewSet

router = DefaultRouter()
router.register(r'', StudentScoreViewSet, basename='grades')

urlpatterns = [
    path('', include(router.urls)),
]
