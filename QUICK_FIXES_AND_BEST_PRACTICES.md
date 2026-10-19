# Quick Fixes & Best Practices for APAR Learning

## 🔧 Immediate Improvements (Can be applied now)

### 1. Add Error Handling in Views

**File**: `authentication/views.py` - Improve dashboard view

```python
@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, "User profile not found. Please complete your profile.")
        return redirect('profile_edit')
    
    context = {'role': profile.role}
    
    try:
        if profile.role == 'admin':
            # Admin dashboard code
            pass
        elif profile.role == 'instructor':
            # Instructor dashboard code
            pass
        else:
            # Student dashboard code
            pass
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        messages.error(request, "An error occurred while loading the dashboard.")
        return redirect('home')
    
    return render(request, 'dashboard.html', context)
```

### 2. Add Input Validation

**File**: `authentication/views.py` - Improve registration view

```python
from django.core.exceptions import ValidationError
import re

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already taken')
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        elif password != password_confirm:
            errors.append('Passwords do not match')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html')
        
        try:
            user = User.objects.create_user(username=username, password=password)
            # Create profile
            Profile.objects.create(user=user, role='student')
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register.html')
```

### 3. Add Database Query Optimization

**File**: `authentication/views.py` - Use select_related and prefetch_related

```python
from django.db.models import Prefetch

@login_required
def dashboard(request):
    # Optimized query
    user = User.objects.select_related('profile').get(id=request.user.id)
    profile = user.profile
    
    if profile.role == 'admin':
        # Use select_related for foreign keys, prefetch_related for reverse
        courses = Course.objects.select_related('instructor').prefetch_related('enrollments')
        context['total_courses'] = len(courses)
    
    elif profile.role == 'instructor':
        courses = Course.objects.filter(instructor=request.user).prefetch_related(
            Prefetch('enrollments', queryset=Enrollment.objects.select_related('student'))
        )
        context['courses'] = courses
    
    return render(request, 'dashboard.html', context)
```

### 4. Add Pagination to List Views

**File**: `course_management/views.py` - Example pagination

```python
from django.core.paginator import Paginator

def course_list_view(request):
    courses = Course.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(courses, 10)  # 10 courses per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'courses': page_obj.object_list,
        'total_courses': paginator.count,
    }
    
    return render(request, 'course_list.html', context)
```

### 5. Add Logging

**File**: `settings.py` - Add logging configuration

```python
import logging
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'formatter': 'verbose',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'app': {
            'handlers': ['console', 'file', 'debug_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
```

### 6. Add CSRF and Security

**File**: `settings.py` - Add security settings

```python
# CSRF Protection
CSRF_COOKIE_SECURE = not DEBUG  # True in production
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# Session Security
SESSION_COOKIE_SECURE = not DEBUG  # True in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),
}

# Password Validation (already configured, but here for reference)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### 7. Add API Standardization

**File**: Create `apar_learning/api_utils.py`

```python
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class APIResponse:
    """Standardized API response"""
    
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        return Response({
            'success': True,
            'message': message,
            'data': data,
        }, status=status_code)
    
    @staticmethod
    def error(error=None, message="Error", status_code=400):
        return Response({
            'success': False,
            'message': message,
            'error': error,
        }, status=status_code)
    
    @staticmethod
    def paginated(data, page, total_pages, total_count, message="Success"):
        return Response({
            'success': True,
            'message': message,
            'data': data,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_count': total_count,
            }
        }, status=200)

# Usage in views:
from apar_learning.api_utils import APIResponse

def api_endpoint(request):
    try:
        data = get_some_data()
        return APIResponse.success(data=data, message="Data retrieved successfully")
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return APIResponse.error(error=str(e), message="Failed to retrieve data", status_code=500)
```

### 8. Add Custom Managers for Queries

**File**: `authentication/models.py` - Add custom manager

```python
from django.db import models
from django.contrib.auth.models import User

class ProfileManager(models.Manager):
    def get_admin_profiles(self):
        return self.filter(role='admin')
    
    def get_instructor_profiles(self):
        return self.filter(role='instructor')
    
    def get_student_profiles(self):
        return self.filter(role='student')
    
    def get_verified_emails(self):
        return self.filter(is_email_verified=True)
    
    def get_incomplete_profiles(self):
        return self.filter(bio__isnull=True) | self.filter(avatar__isnull=True)

class Profile(models.Model):
    # ... existing fields ...
    
    objects = ProfileManager()  # Add custom manager
```

### 9. Add Template Tags for Common Operations

**File**: Create `authentication/templatetags/auth_tags.py`

```python
from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def user_role_badge(role):
    """Display role as a badge"""
    colors = {
        'admin': 'danger',
        'instructor': 'info',
        'student': 'success',
    }
    color = colors.get(role, 'secondary')
    return format_html(
        '<span class="badge badge-{}">{}</span>',
        color, role.title()
    )

@register.filter
def profile_avatar(user):
    """Display user avatar with fallback"""
    try:
        if user.profile.avatar:
            return user.profile.avatar.url
    except:
        pass
    return '/static/images/default-avatar.png'

@register.filter
def is_profile_complete(user):
    """Check if user profile is complete"""
    try:
        return user.profile.is_complete()
    except:
        return False
```

### 10. Add Management Commands

**File**: Create `authentication/management/commands/create_test_data.py`

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import Profile
from course_management.models import Course

class Command(BaseCommand):
    help = 'Create test data for development'
    
    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data')
    
    def handle(self, *args, **options):
        if options['clear']:
            User.objects.filter(username__startswith='test_').delete()
            self.stdout.write(self.style.WARNING('Cleared test users'))
        
        # Create test admin
        admin_user, created = User.objects.get_or_create(
            username='test_admin',
            defaults={'email': 'admin@test.com', 'is_staff': True}
        )
        if created:
            admin_user.set_password('test123')
            admin_user.save()
        Profile.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})
        
        # Create test instructor
        instructor_user, created = User.objects.get_or_create(
            username='test_instructor',
            defaults={'email': 'instructor@test.com'}
        )
        if created:
            instructor_user.set_password('test123')
            instructor_user.save()
        Profile.objects.get_or_create(user=instructor_user, defaults={'role': 'instructor'})
        
        # Create test students
        for i in range(5):
            student_user, created = User.objects.get_or_create(
                username=f'test_student_{i}',
                defaults={'email': f'student{i}@test.com'}
            )
            if created:
                student_user.set_password('test123')
                student_user.save()
            Profile.objects.get_or_create(user=student_user, defaults={'role': 'student'})
        
        # Create test course
        course, created = Course.objects.get_or_create(
            title='Introduction to Django',
            defaults={
                'description': 'Learn Django basics',
                'instructor': instructor_user
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully'))
```

Usage:
```bash
python manage.py create_test_data
python manage.py create_test_data --clear
```

---

## 🔐 Security Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure CSRF protection
- [ ] Set secure session cookies
- [ ] Implement rate limiting
- [ ] Add input validation on all forms
- [ ] Use parameterized queries (Django ORM handles this)
- [ ] Sanitize user input
- [ ] Add authentication to all views
- [ ] Implement proper permission checks
- [ ] Keep dependencies updated
- [ ] Use strong passwords
- [ ] Enable security headers
- [ ] Log security events

---

## 📊 Performance Checklist

- [ ] Use select_related() for ForeignKey
- [ ] Use prefetch_related() for reverse relations
- [ ] Add database indexes for frequently queried fields
- [ ] Use database transactions for atomic operations
- [ ] Implement caching (Redis)
- [ ] Optimize images (compress, resize)
- [ ] Use CDN for static files
- [ ] Enable gzip compression
- [ ] Minimize database queries
- [ ] Use pagination for large result sets
- [ ] Profile views with django-debug-toolbar
- [ ] Monitor query performance
- [ ] Use async views for long operations
- [ ] Implement lazy loading
- [ ] Remove unused middleware

---

## 📝 Code Quality Standards

### Naming Conventions
```python
# Models
class UserProfile(models.Model):  # CamelCase, singular
    pass

# Fields
created_at = models.DateTimeField(auto_now_add=True)  # snake_case
is_verified = models.BooleanField(default=False)  # Boolean prefix with 'is_'

# Methods
def get_full_name(self):  # snake_case, verb prefix
    pass

# Constants
MAX_UPLOAD_SIZE = 5242880  # UPPERCASE_WITH_UNDERSCORES
ROLE_CHOICES = [...]  # Plural for choices

# Private methods
def _process_data(self):  # Leading underscore
    pass
```

### Docstring Style
```python
def calculate_average(values):
    """
    Calculate the average of a list of values.
    
    Args:
        values (list): List of numeric values.
    
    Returns:
        float: The average value.
    
    Raises:
        ValueError: If values list is empty.
    """
    if not values:
        raise ValueError("Values list cannot be empty")
    return sum(values) / len(values)
```

### Comment Style
```python
# Use comments sparingly, prefer clear code
# Bad:
x = y + 1  # Increment y by 1

# Good:
next_page_number = current_page + 1

# Good comment:
# Cache is invalidated when course is updated to ensure fresh data
cache.delete(f'course_{course_id}')
```

---

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Run `python manage.py check --deploy`
- [ ] Set `SECRET_KEY` in environment variable
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up database backups
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Enable security middleware
- [ ] Configure CDN for static files
- [ ] Set up SSL certificate
- [ ] Configure web server (Gunicorn/uWSGI)
- [ ] Set up supervisor/systemd
- [ ] Configure monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Document deployment steps

---

## 📚 Resources

- Django Best Practices: https://docs.djangoproject.com/en/stable/
- Security: https://docs.djangoproject.com/en/stable/topics/security/
- Performance: https://docs.djangoproject.com/en/stable/topics/performance/
- Testing: https://docs.djangoproject.com/en/stable/topics/testing/

