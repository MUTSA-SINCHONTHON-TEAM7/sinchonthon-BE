from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Review
from .serializers import *
from lectures.models import Lecture

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review(request):
  match request.method:
    case 'POST':
      serializer = PostReviewSerializer(data=request.data)
      if serializer.is_valid():
        lecture = Lecture.objects.get(id=request.data['lecture_id'])
        
        review = Review.objects.create(
          mutsa_user=request.user,
          lecture=lecture,
          content=serializer.validated_data['content']
        )
        
        responseSerializer = GetReviewSerializer(review)
        return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST1)
    
    case 'GET':
      try:
        lecid = request.GET.get('lectureId', None)
        reviews = Review.objects.filter(lecture=lecid)
        review_serializer = GetReviewSerializer(reviews, many=True)
        return Response(review_serializer.data, status=status.HTTP_200_OK)
      except:
        return Response({"error": "리뷰가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def review_delete(request, id):
  try:
    review = Review.objects.get(id=id)
  except:
    return Response({"error": "해당 리뷰가 없습니다!"}, status=status.HTTP_404_NOT_FOUND)
  review.delete()
  return Response({"message": "리뷰 삭제 성공"}, status=status.HTTP_200_OK)