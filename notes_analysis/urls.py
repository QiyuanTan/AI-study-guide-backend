from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
]
