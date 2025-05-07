# -*- coding = utf-8 -*-
# @Time : 2025/5/1 20:50
# @File : serializers
from rest_framework import serializers
from .models import Note, Course

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

