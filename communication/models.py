from django.db import models
from django.contrib.auth.models import User
from course_management.models import Course


class Message(models.Model):

    MESSAGE_STATUS = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='course_messages')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    # Enhanced fields
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=MESSAGE_STATUS, default='sent')
    
    # Threading
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_receiver = models.BooleanField(default=False)
    
    # Attachments
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    attachment_type = models.CharField(max_length=50, blank=True, null=True)
    
    # Metadata
    edited_at = models.DateTimeField(blank=True, null=True)
    is_edited = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High')],
        default='normal'
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sender', 'receiver', 'sent_at']),
            models.Index(fields=['receiver', 'is_read']),
        ]

    def __str__(self):
        return f'From {self.sender.username} to {self.receiver.username} - {self.sent_at.strftime("%Y-%m-%d %H:%M")}'

    def mark_as_read(self):
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.status = 'read'
            self.save()

    def get_thread_messages(self):
        """Get all messages in this thread"""
        if self.parent_message:
            return self.parent_message.get_thread_messages()
        return Message.objects.filter(
            models.Q(id=self.id) | models.Q(parent_message=self)
        ).order_by('sent_at')

    def get_reply_count(self):
        return self.replies.count()


class MessageAttachment(models.Model):

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='message_attachments/')
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # in bytes
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message Attachment"
        verbose_name_plural = "Message Attachments"

    def __str__(self):
        return f'{self.file_name} - {self.message}'


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('assignment', 'Assignment Update'),
        ('course', 'Course Update'),
        ('grade', 'Grade Posted'),
        ('comment', 'New Comment'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notifier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications_sent')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    related_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.notification_type} - {self.recipient.username}'

    def mark_as_read(self):
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
