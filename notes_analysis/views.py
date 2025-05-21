import json
import os
import subprocess

from django.contrib.admin.templatetags.admin_list import results
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
            saved_question.answer = question['correct_option'] if question['question_type'] == 'mcq' else question['starter_code']
            saved_question.type = question['question_type']

            saved_question.save()

            if question['question_type'] == 'code':
                # save autograder
                autograder_script = question['autograder_script']

                autograder_dir = f'autograders/{i}'
                os.makedirs(autograder_dir, exist_ok=True)

                with open(f'{autograder_dir}/autograder.py', 'w', encoding='utf-8') as f:
                    f.write(autograder_script)

            question.pop("correct_option", None)
            question.pop("sample_code", None)
            question.pop("sample_input_output", None)
            question.pop("autograder_script", None)
            question.pop("explanation", None)

        print(json.dumps(questions))

        return Response(questions)


    @action(detail=True, methods=['post'])
    def submit_quiz(self, request, pk=None):
        submitted_data = request.data['submission']
        saved_questions = Question.objects.all()
        result = []

        for i, (question, saved_question) in enumerate(zip(submitted_data, saved_questions)):
            if saved_question.type == 'mcq':
                result.append({'correct': question['answer'] == saved_question.answer, 'correct_option': saved_question.answer})
            else:
                # save student's code
                autograder_path = f'autograders/{i}'
                with open(f'{autograder_path}/student_submission.txt', 'w', encoding='utf-8') as f:
                    f.write(question['answer'])

                process = subprocess.run(["python",
                                          "autograder.py",
                                          "student_submission.txt"], capture_output=True, text=True, cwd=autograder_path)

                result.append({'correct': process.returncode == 0, 'correct_option': ''})

                print(f'autograded exited with return code: {process.returncode}')
                print(process.stdout)

        Question.objects.all().delete()

        return Response({'results': result})

class NoteViewSet(viewsets.ModelViewSet):
    queryset=Note.objects.all()
    serializer_class = NoteSerializer
