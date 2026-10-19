from django.db import models

from django.contrib.auth.models import User

class Course(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    image = models.ImageField(upload_to='courses/', null=True, blank=True)

    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.title

class Enrollment(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('student', 'course')

    def __str__(self):

        return f'{self.student.username} in {self.course.title}'
