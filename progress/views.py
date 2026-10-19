from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Progress
from content_management.models import Content

@login_required
def mark_completed(request, content_id):
    try:
        content = get_object_or_404(Content, id=content_id)
        
        # Verify student is enrolled in course
        from course_management.models import Enrollment
        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=content.course
        ).first()
        
        if not enrollment and request.user.profile.role == 'student':
            messages.error(request, 'You must be enrolled in this course.')
            return redirect('course_list')
        
        progress, created = Progress.objects.get_or_create(
            student=request.user,
            course=content.course,
            content=content,
            defaults={'completed': True}
        )
        
        if not created:
            progress.completed = True
            progress.save()
        
        messages.success(request, f'Marked {content.title} as completed!')
        return redirect('course_detail', course_id=content.course.id)
    except Content.DoesNotExist:
        messages.error(request, 'Content not found.')
        return redirect('course_list')
