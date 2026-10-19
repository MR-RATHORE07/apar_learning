from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Case, When, BooleanField, Value
from .models import Course, Enrollment
from .forms import CourseForm

@login_required
def course_list(request):
    courses = Course.objects.all().distinct()
    if request.user.profile.role == 'student':
        # Annotate courses with enrollment status for the current student
        courses = courses.annotate(
            is_enrolled=Case(
                When(enrollments__student=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
    else:
        # For non-students, mark all as "enrolled" (they can view all)
        courses = courses.annotate(is_enrolled=Value(True))

    # Remove duplicate courses with the same title to avoid repeated course cards
    seen_titles = set()
    unique_courses = []
    for course in courses:
        if course.title not in seen_titles:
            seen_titles.add(course.title)
            unique_courses.append(course)

    return render(request, 'course_list.html', {
        'courses': unique_courses,
        'page_title': 'Available Courses',
        'empty_message': 'No courses available.',
    })


@login_required
def my_courses(request):
    role = request.user.profile.role
    if role == 'student':
        courses = Course.objects.filter(enrollments__student=request.user)
        empty_message = "You haven't enrolled in any courses yet."
    elif role == 'instructor':
        courses = Course.objects.filter(instructor=request.user)
        empty_message = "You haven't created any courses yet."
    else:
        courses = Course.objects.all()
        empty_message = 'No courses are available yet.'

    courses = courses.annotate(is_enrolled=Value(True, output_field=BooleanField()))
    return render(request, 'course_list.html', {
        'courses': courses.distinct(),
        'page_title': 'My Courses',
        'empty_message': empty_message,
    })

@login_required
def course_detail(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        assignments = course.assignments.all()
        contents = course.contents.all()
        quizzes = course.quizzes.all()
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists() if request.user.profile.role == 'student' else True

        # Add progress information for each content if user is student
        if request.user.profile.role == 'student' and is_enrolled:
            from progress.models import Progress
            for content in contents:
                content.progress = Progress.objects.filter(
                    student=request.user,
                    content=content
                ).first()

        context = {
            'course': course,
            'assignments': assignments,
            'contents': contents,
            'quizzes': quizzes,
            'is_enrolled': is_enrolled
        }
        return render(request, 'course_detail.html', context)
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_list')

@login_required
def create_course(request):
    if request.user.profile.role != 'instructor':
        messages.error(request, 'Only instructors can create courses.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

@login_required
def enroll_course(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        if request.user.profile.role == 'student':
            enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
            if created:
                messages.success(request, f'Successfully enrolled in {course.title}!')
            else:
                messages.info(request, 'You are already enrolled in this course.')
        else:
            messages.warning(request, 'Only students can enroll in courses.')
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
    
    return redirect('course_list')
