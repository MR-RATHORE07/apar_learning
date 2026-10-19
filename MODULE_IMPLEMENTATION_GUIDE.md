# Module Enhancement Roadmap

## 🎯 Priority: HIGH - Implement Empty Modules

### Module 1: Admin Management
**Purpose**: Platform administration and system-wide configurations

```python
# admin_management/models.py

from django.db import models
from django.contrib.auth.models import User

class AdminLog(models.Model):
    """Track all admin actions for audit trail"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='admin_logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=100)  # What was changed
    object_id = models.PositiveIntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Admin Log"
        verbose_name_plural = "Admin Logs"

class SystemSettings(models.Model):
    """Platform-wide settings"""
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.setting_key

class UserApproval(models.Model):
    """Instructor approval workflow"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualifications = models.TextField()
    experience = models.IntegerField()  # years
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                   related_name='approvals_reviewed', blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### Module 2: Instructor Management
**Purpose**: Advanced instructor features and analytics

```python
# instructor_management/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from course_management.models import Course

class InstructorSchedule(models.Model):
    """Teaching schedule for instructors"""
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=[(i, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i]) for i in range(7)])
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ('instructor', 'day_of_week', 'start_time')

class CoursePerformance(models.Model):
    """Analytics for each course"""
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='performance')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    total_enrolled = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0)
    average_rating = models.FloatField(default=0)
    student_satisfaction = models.FloatField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def calculate_metrics(self):
        """Calculate performance metrics"""
        from course_management.models import Enrollment
        from feedback.models import Feedback
        
        enrollments = Enrollment.objects.filter(course=self.course)
        self.total_enrolled = enrollments.count()
        
        # Completion rate
        completed = enrollments.filter(student__progress__completed=True).count()
        self.completion_rate = (completed / self.total_enrolled * 100) if self.total_enrolled > 0 else 0
        
        # Average rating
        feedbacks = Feedback.objects.filter(course=self.course)
        avg = feedbacks.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = avg or 0
        
        self.save()

class InstructorCertification(models.Model):
    """Instructor qualifications and certifications"""
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-issue_date']
```

---

### Module 3: Student Management
**Purpose**: Advanced student features and progress tracking

```python
# student_management/models.py

from django.db import models
from django.contrib.auth.models import User
from course_management.models import Course

class StudentProfile(models.Model):
    """Extended student profile"""
    EDUCATION_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    current_gpa = models.FloatField(default=0, help_text="0.0 to 4.0")
    learning_style = models.CharField(max_length=100, blank=True)  # Visual, Auditory, Reading/Writing, Kinesthetic
    goals = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StudentBadge(models.Model):
    """Achievement badges for students"""
    BADGE_TYPES = [
        ('completion', 'Course Completion'),
        ('excellence', 'Academic Excellence'),
        ('consistency', 'Consistency'),
        ('participation', 'Active Participation'),
        ('helper', 'Peer Helper'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'badge_type')

class StudentCertificate(models.Model):
    """Certificates earned by students"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=100, unique=True)
    completion_percentage = models.FloatField()
    issue_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "Student Certificate"
        verbose_name_plural = "Student Certificates"
```

---

### Module 4: Progress Tracking (Extended)
**Purpose**: Advanced analytics and insights

```python
# progress_tracking/models.py

from django.db import models
from django.contrib.auth.models import User
from course_management.models import Course
from content_management.models import Content

class DetailedProgress(models.Model):
    """Detailed tracking of learning progress"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    
    time_spent = models.DurationField(default=0)  # Total time on content
    view_count = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    completion_percentage = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'content')
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['student', 'is_completed']),
        ]

class LearningMetrics(models.Model):
    """Overall learning metrics for a student"""
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learning_metrics')
    
    total_courses_enrolled = models.IntegerField(default=0)
    total_courses_completed = models.IntegerField(default=0)
    total_learning_hours = models.FloatField(default=0)
    average_completion_time = models.FloatField(default=0, help_text="in hours")
    skill_tags = models.JSONField(default=list)  # ["Python", "Django", "Web Dev"]
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_metrics(self):
        """Recalculate learning metrics"""
        from course_management.models import Enrollment
        
        enrollments = Enrollment.objects.filter(student=self.student)
        self.total_courses_enrolled = enrollments.count()
        
        # Calculate completed courses
        completed = enrollments.filter(student__progress__completed=True).distinct().count()
        self.total_courses_completed = completed
        
        self.save()
```

---

### Module 5: Communication Notification
**Purpose**: Multi-channel notification delivery

```python
# communication_notification/models.py

from django.db import models
from django.contrib.auth.models import User
from communication.models import Notification

class NotificationPreference(models.Model):
    """User notification preferences"""
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_prefs')
    
    # Channel preferences
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    
    # Notification frequency
    immediate = models.BooleanField(default=True)  # Send immediately
    digest_frequency = models.CharField(
        max_length=10,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('never', 'Never')],
        default='never'
    )
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_start = models.TimeField(null=True, blank=True)
    quiet_end = models.TimeField(null=True, blank=True)

class NotificationLog(models.Model):
    """Log of all sent notifications"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=NotificationPreference.CHANNEL_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-sent_at']
```

---

### Module 6: Feedback Support
**Purpose**: Help desk and support ticket system

```python
# feedback_support/models.py

from django.db import models
from django.contrib.auth.models import User

class SupportTicket(models.Model):
    """Help desk support tickets"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_customer', 'Waiting Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('technical', 'Technical Issue'),
        ('content', 'Content Issue'),
        ('account', 'Account Issue'),
        ('billing', 'Billing'),
        ('other', 'Other'),
    ]
    
    ticket_id = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_tickets', limit_choices_to={'groups__name': 'Support Staff'})
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"

class TicketResponse(models.Model):
    """Responses to support tickets"""
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='support_attachments/', blank=True, null=True)
    
    is_internal = models.BooleanField(default=False)  # Only visible to staff
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
```

---

## 📋 Migration Commands

After implementing each module:

```bash
# Create migrations
python manage.py makemigrations admin_management
python manage.py makemigrations instructor_management
python manage.py makemigrations student_management
python manage.py makemigrations progress_tracking
python manage.py makemigrations communication_notification
python manage.py makemigrations feedback_support

# Apply migrations
python manage.py migrate

# Create superuser if needed
python manage.py createsuperuser

# Register models in admin
# Update admin.py files in each module
```

---

## 🔗 Model Relationships Summary

```
User (Django Auth)
├── Profile (Authentication)
├── Student Profile (Student Management)
├── Learning Metrics (Progress Tracking)
├── Notification Preferences (Communication Notification)
├── Admin Logs (Admin Management)
├── Support Tickets (Feedback Support)
└── ...Courses, Messages, etc.

Course (Course Management)
├── Enrollments
├── Contents
├── Assignments
├── Quizzes
├── Feedback
├── Course Performance (Instructor Management)
└── Certificates (Student Management)

Enrollment (Course Management)
└── Progress (Progress)
```

---

## ✅ Testing Checklist for New Modules

- [ ] Create model tests
- [ ] Test signal handlers
- [ ] Test admin interface
- [ ] Test API endpoints
- [ ] Test permissions and access control
- [ ] Test cascading deletes
- [ ] Test data migrations
- [ ] Test edge cases and boundaries

