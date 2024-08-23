from rest_framework import serializers

from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'mutsa_user_id', 'lecture_id', 'content']

class GetReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'mutsa_user_id', 'content']