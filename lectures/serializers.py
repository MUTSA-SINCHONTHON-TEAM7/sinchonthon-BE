from rest_framework import serializers
from .models import Lecture, Fundings

class LectureResponseSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source='subject.id')
    writer_nickname = serializers.CharField(source='mutsa_user.nickname')
    funding_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lecture
        fields = ['id', 'subject_id', 'title', 'category', 'cost', 'min_total_cost', 'max_student', 'lecture_detail', 'writer_nickname', 'funding_count']
        
    def get_funding_count(self, obj):
        return Fundings.objects.filter(lecture=obj).count()
        
class LecturePostSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()
    title = serializers.CharField()
    cost = serializers.IntegerField()
    min_total_cost = serializers.IntegerField()
    max_student = serializers.IntegerField()
    lecture_detail = serializers.CharField()
    category = serializers.CharField()
    
class FundingPostSerializer(serializers.Serializer):
    lecture_id = serializers.IntegerField()
    
class FundingResponseSerializer(serializers.ModelSerializer):
    funding_id = serializers.IntegerField(source='id')
    mutsa_user_id = serializers.IntegerField(source='mutsa_user.id')
    lecture_id = serializers.IntegerField(source='lecture.id')
    
    class Meta:
        model = Fundings
        fields = ['funding_id', 'mutsa_user_id', 'lecture_id']