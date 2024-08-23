from rest_framework import generics
from .models import Subject, Votes
from .serializers import SubjectPostSerializer, SubjectResponseSerializer, VotePostSerializer, VoteResponseSerializer, FundSubjectResponseSerializer, SubjectAndVoteResponseSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subject_post(request):
    serializer = SubjectPostSerializer(data=request.data)
    if serializer.is_valid(): 
        createSubject = Subject.objects.create(
            name=serializer.validated_data['name'],
            category=serializer.validated_data['category'],
            subject_detail=serializer.validated_data['subject_detail']
        )
        
        responseSerializer = SubjectResponseSerializer(createSubject)
        return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def vote_access(request):
    if request.method == 'POST':
        serializer = VotePostSerializer(data=request.data)
        if serializer.is_valid():
            subject_id = serializer.validated_data['subject_id']
            if Votes.objects.filter(subject__id=subject_id, mutsa_user=request.user).exists():
                return Response('이미 이 항목에 투표하셨습니다.', status=status.HTTP_400_BAD_REQUEST)
            try:
                createSubject = Votes.objects.create(
                    subject=Subject.objects.get(id=subject_id),
                    mutsa_user = request.user
                )
                responseSerializer = VoteResponseSerializer(createSubject)
                return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
            except Subject.DoesNotExist:
                return Response('항목을 찾을 수 없습니다.', status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        serializer = VotePostSerializer(data=request.data)
        if serializer.is_valid(): 
            try:
                subject_id = serializer.validated_data['subject_id'] 
                vote = Votes.objects.filter(
                    subject=Subject.objects.get(id=subject_id),
                    mutsa_user=request.user
                )
                vote.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Subject.DoesNotExist:
                return Response('항목을 찾을 수 없습니다.', status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_fundsubjects(request):
    category = request.GET.get("category", None)
    subjects = []

    if category:
        subjects = Subject.objects.filter(category=category)
    else:
        subjects = Subject.objects.all()
        
    subjects = [s for s in subjects if Votes.objects.filter(subject=s).count() >= 50]
    serializer = FundSubjectResponseSerializer(subjects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_votesubjects(request):
    category = request.GET.get("category", None)
    subjects = []

    if category:
        subjects = Subject.objects.filter(category=category)
    else:
        subjects = Subject.objects.all()

    subjects = [s for s in subjects if Votes.objects.filter(subject=s).count() < 50]

    serializer = SubjectAndVoteResponseSerializer(subjects, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
