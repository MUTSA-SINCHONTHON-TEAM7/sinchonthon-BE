from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Lecture, Fundings
from subjects.models import Subject
from .serializers import LectureResponseSerializer, LecturePostSerializer, FundingPostSerializer, FundingResponseSerializer

# Create your views here.

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def lecture_post_or_lists(request):
    if request.method == 'GET':
        subjectId = request.GET.get("subjectId", None)
        category = request.GET.get("category", None)
        
        lectures = None
        if subjectId is not None:
            subject = None
            try:
                subject = Subject.objects.get(id=int(subjectId))
            except Subject.DoesNotExist:
                return Response('없는 주제입니다.', status=status.HTTP_404_NOT_FOUND)
            lectures = Lecture.objects.filter(subject=subject)
        elif category is not None:
            lectures = Lecture.objects.filter(category=category)
        
        serializer = LectureResponseSerializer(lectures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.user == None:
            return Response('인증 헤더가 필요합니다.', status=status.HTTP_401_UNAUTHORIZED)
    
        serializer = LecturePostSerializer(data=request.data)
        if serializer.is_valid():
            subject = None
            try:
                subject = Subject.objects.get(id=serializer.validated_data['subject_id'])
            except Subject.DoesNotExist:
                return Response('없는 주제입니다.', status=status.HTTP_404_NOT_FOUND)
            createdLecture = Lecture.objects.create(
                subject=subject,
                mutsa_user=request.user,
                title=serializer.validated_data['title'],
                category=serializer.validated_data['category'],
                cost=serializer.validated_data['cost'],
                min_total_cost=serializer.validated_data['min_total_cost'],
                max_student=serializer.validated_data['max_student'],
                lecture_detail=serializer.validated_data['lecture_detail']
            )
            responseSerializer = LectureResponseSerializer(createdLecture)
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
def lecture_single(request, id):
    if request.method == 'GET':
        try:
            lecture = Lecture.objects.get(id=id)
            serializer = LectureResponseSerializer(lecture)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lecture.DoesNotExist:
            return Response('없는 강의입니다.', status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        try:
            lecture = Lecture.objects.get(id=id)
            if lecture.mutsa_user != request.user:
                return Response('당신의 강의가 아닙니다.', status=status.HTTP_403_FORBIDDEN)
            lecture.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Lecture.DoesNotExist:
            return Response('없는 강의입니다.', status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecture_my(requset):
    lectures = Lecture.objects.filter(mutsa_user=requset.user)
    serializer = LectureResponseSerializer(lectures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecture_applied(request):
    fundings = Fundings.objects.filter(mutsa_user=request.user)
    lectures = []
    
    for f in fundings:
        lectures.append(f.lecture)
    
    serializer = LectureResponseSerializer(lectures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def funding_access(request):
    if request.method == 'POST':
        serializer = FundingPostSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                funding = Fundings.objects.create(
                    mutsa_user=request.user,
                    lecture=Lecture.objects.get(id=serializer.validated_data['lecture_id'])
                )
                responseSerializer = FundingResponseSerializer(funding)
                return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
            except Lecture.DoesNotExist:
                return Response('없는 강의입니다.', status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        serializer = FundingPostSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                Fundings.objects.filter(
                    lecture=Lecture.objects.get(id=serializer.validated_data['lecture_id']),
                    mutsa_user=request.user
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Lecture.DoesNotExist:
                return Response('없는 강의입니다.', status=status.HTTP_404_NOT_FOUND)