from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, NoteViewSet

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'note', NoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]
