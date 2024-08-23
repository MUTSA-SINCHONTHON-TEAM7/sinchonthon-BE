from rest_framework import serializers

from subjects.models import Subject
from lectures.models import Lecture

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'category']

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'category']

class SubLecSerializer(serializers.Serializer):
    subList = SubjectSerializer(many=True)
    lecList = LectureSerializer(many=True)