from rest_framework import serializers
from .models import Meeting, Translation

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'host', 'created_at', 'is_active']

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'meeting', 'user', 'text', 'created_at']