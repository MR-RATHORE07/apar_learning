from rest_framework import serializers
from .models import Content

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'course', 'title', 'content_type', 'file', 'url', 'video_url', 'description', 'order', 'created_at']
