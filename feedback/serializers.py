from rest_framework import serializers
from .models import Feedback
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class FeedbackSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'student', 'course', 'rating', 'comment', 'submitted_at']
