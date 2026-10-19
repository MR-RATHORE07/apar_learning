from rest_framework import serializers
from .models import Course, Enrollment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    enrollments = serializers.IntegerField(source='enrollments.count', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'image', 'instructor', 'created_at', 'updated_at', 'enrollments']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
