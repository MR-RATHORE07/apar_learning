from django.db import models

from django.contrib.auth.models import User

from course_management.models import Course

class Feedback(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5

    comment = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.student.username} - {self.course.title} - {self.rating}'
