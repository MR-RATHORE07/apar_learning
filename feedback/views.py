from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from course_management.models import Course, Enrollment

@login_required
def submit_feedback(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
        
        if not enrollment:
            messages.error(request, 'You must be enrolled in this course to submit feedback.')
            return redirect('course_list')
        
        # Check if feedback already exists
        existing_feedback = Feedback.objects.filter(student=request.user, course=course).first()
        
        if request.method == 'POST':
            form = FeedbackForm(request.POST, instance=existing_feedback)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.student = request.user
                feedback.course = course
                feedback.save()
                messages.success(request, 'Feedback submitted successfully!')
                return redirect('course_detail', course_id=course.id)
            else:
                messages.error(request, 'Please fix the errors below.')
        else:
            form = FeedbackForm(instance=existing_feedback)
        
        return render(request, 'submit_feedback.html', {'form': form, 'course': course})
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_list')
