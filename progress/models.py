from django.db import models

from django.contrib.auth.models import User

from course_management.models import Course

from content_management.models import Content

class Progress(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        unique_together = ('student', 'content')

    def __str__(self):

        return f'{self.student.username} - {self.content.title}'
