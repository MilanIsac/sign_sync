from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Meeting, Translation
from .serializers import MeetingSerializer, TranslationSerializer
from .tasks import process_video_feed
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

sign_model = load_model('ml_model/sign_language_model.h5')

@api_view(['POST'])
def create_meeting(request):
    serializer = MeetingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(host=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def process_sign_language(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    video_file = request.FILES.get('video')
    task = process_video_feed.delay(video_file.temporary_file_path(), meeting.id, request.user.id)
    return Response({'task_id': task.id}, status=202)