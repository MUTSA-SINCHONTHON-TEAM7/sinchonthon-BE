from rest_framework import serializers

from .models import Review

class PostReviewSerializer(serializers.Serializer):
    lecture_id = serializers.IntegerField(),
    content = serializers.CharField()

class GetReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'mutsa_user_id', 'content']