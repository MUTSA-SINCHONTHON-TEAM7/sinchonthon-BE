from rest_framework import serializers
from .models import Subject, CategoryChoices, Votes

class SubjectResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'category', 'subject_detail']

class SubjectAndVoteResponseSerializer(serializers.ModelSerializer):
    vote = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'category', 'subject_detail', 'vote']
    
    def get_vote(self, obj):
        return Votes.objects.filter(subject=obj).count()

class FundSubjectResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'category', 'subject_detail']

class SubjectPostSerializer(serializers.Serializer):
    name = serializers.CharField()
    subject_detail = serializers.CharField()
    category = serializers.CharField()

class VotePostSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()

class VoteResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ['id', 'mutsa_user', 'subject']
