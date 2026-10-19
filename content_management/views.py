from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Content, StudentNote
from .forms import ContentForm, StudentNoteForm
from course_management.models import Course
from progress.models import Progress

@login_required
def add_content(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        if request.method == 'POST':
            form = ContentForm(request.POST, request.FILES)
            if form.is_valid():
                content = form.save(commit=False)
                content.course = course
                content.save()
                messages.success(request, 'Content added successfully!')
                return redirect('course_detail', course_id=course.id)
            else:
                messages.error(request, 'Please fix the errors below.')
        else:
            form = ContentForm()
        return render(request, 'add_content.html', {'form': form, 'course': course})
    except Course.DoesNotExist:
        messages.error(request, 'Course not found or you do not have permission to edit it.')
        return redirect('course_list')

@login_required
def content_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    course = content.course

    # Check if user has access to this content
    if request.user.profile.role == 'student':
        from course_management.models import Enrollment
        enrollment = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not enrollment:
            messages.error(request, 'You must be enrolled in this course to view content.')
            return redirect('course_list')

    # Get or create progress
    progress, created = Progress.objects.get_or_create(
        student=request.user,
        course=course,
        content=content,
        defaults={'completed': False}
    )

    # Get student's notes
    student_note = None
    if request.user.profile.role == 'student':
        student_note = StudentNote.objects.filter(student=request.user.profile, content=content).first()

    if request.method == 'POST' and request.user.profile.role == 'student':
        note_form = StudentNoteForm(request.POST, instance=student_note)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.student = request.user.profile
            note.content = content
            note.save()
            messages.success(request, 'Note saved successfully!')
            return redirect('content_detail', content_id=content.id)
    else:
        note_form = StudentNoteForm(instance=student_note)

    context = {
        'content': content,
        'course': course,
        'progress': progress,
        'note_form': note_form,
        'student_note': student_note,
    }
    return render(request, 'content_detail.html', context)

@login_required
def save_note(request, content_id):
    if request.method == 'POST' and request.user.profile.role == 'student':
        content = get_object_or_404(Content, id=content_id)
        note_text = request.POST.get('note_text', '')

        note, created = StudentNote.objects.get_or_create(
            student=request.user.profile,
            content=content,
            defaults={'note_text': note_text}
        )

        if not created:
            note.note_text = note_text
            note.save()

        return JsonResponse({'success': True, 'message': 'Note saved successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
