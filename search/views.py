from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from subjects.models import Subject
from lectures.models import Lecture
from .serializers import SubLecSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
  search_word = request.GET.get('search')
  
  try:
    subList = Subject.objects.filter(name__icontains=search_word)
    lecList = Lecture.objects.filter(title__icontains=search_word)
    data = {
      'subList' : subList,
      'lecList' : lecList,
    }
    serializer = SubLecSerializer(instance=data)
    return Response(serializer.data)
  
  except:
    return Response({"error": "검색 결과가 없습니다!"}, status=status.HTTP_404_NOT_FOUND)
  