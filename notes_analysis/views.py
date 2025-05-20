from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import CourseSerializer
from .serializers import NoteSerializer
from .utils.analyze_notes import generate_questions
from .utils.obj2json import *

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'])
    def generate_quiz(self, request, pk=None):
        course = self.get_object()
        
        questions = generate_questions(get_notes(course), get_syllabus(course))

        for i, question in enumerate(questions):
            saved_question, created = Question.objects.get_or_create(index = i)
            saved_question.content = question['content']
            saved_question.answer = question['correct_option'] if question['type'] == 'mcq' else question['sample_code']

            saved_question.save()

            if question['type'] == 'code':
                # save autograder
                autograder_script = question['autograder_script']
                with open(f'autograders/{i}/autograder.py', 'w', encoding='utf-8') as f:
                    f.write(autograder_script)

            question.pop("correct_option")
            question.pop("sample_code")
            question.pop("sample_input_output")
            question.pop("autograder_script")

        return Response(questions)


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
