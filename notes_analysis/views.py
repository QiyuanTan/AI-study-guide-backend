from django.shortcuts import render
from rest_framework import viewsets
from .models import Course
from. serializers import CourseSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'])
    def generate_quiz(self, request, pk=None):
        course = self.get_object()
        
        # Placeholder logic
        # In real use, you might trigger some async task or external model
        return Response({
            "message": f"Quiz generation started for course '{course.name}'."
        })

    @action(detail=True, methods=['post'])
    def submit_quiz(self, request, pk=None):
        course = self.get_object()
        submitted_data = request.data.get("answers", {})
        return Response({
            "message": f"Quiz submitted for course '{course.name}'.",
            "received": submitted_data
        })

class NoteViewSet(viewsets.ModelViewSet):
    queryset=Note.objects.all()
    serializer_class = NoteSerializer
