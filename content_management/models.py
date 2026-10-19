from django.db import models

from course_management.models import Course

class Content(models.Model):

    CONTENT_TYPES = [
        ('video', 'Video'),
        ('document', 'Document'),
        ('image', 'Image'),
        ('link', 'Link'),
        ('interactive', 'Interactive'),
        ('text', 'Text Content'),
        ('presentation', 'Presentation'),
        ('audio', 'Audio'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='contents/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)  # For text-based content
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(blank=True, null=True, help_text="Duration in minutes")
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class StudentNote(models.Model):
    student = models.ForeignKey('authentication.Profile', on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'content')

    def __str__(self):
        return f"{self.student.user.username}'s note on {self.content.title}"
