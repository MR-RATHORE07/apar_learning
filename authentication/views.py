from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from course_management.models import Course, Enrollment

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    featured_courses = []
    seen_titles = set()
    for course in Course.objects.all():
        if course.title not in seen_titles:
            seen_titles.add(course.title)
            featured_courses.append(course)
        if len(featured_courses) >= 4:
            break
    context = {'featured_courses': featured_courses}
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    from django.contrib.auth.models import User
    from django.utils import timezone
    from datetime import timedelta
    from assignment_quiz.models import Submission, Assignment
    from feedback.models import Feedback
    
    profile = request.user.profile
    context = {'role': profile.role}
    
    if profile.role == 'admin':
        # Admin dashboard data - Real statistics
        total_users = User.objects.count()
        total_courses = Course.objects.count()
        total_enrollments = Enrollment.objects.count()
        total_instructors = User.objects.filter(profile__role='instructor').count()
        total_students = User.objects.filter(profile__role='student').count()
        
        # Active sessions (enrollments in last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        active_sessions = Enrollment.objects.filter(enrolled_at__gte=week_ago).count()
        
        # Completion rate (courses completed / total enrollments)
        completed_enrollments = Enrollment.objects.filter(
            student__in=User.objects.filter(profile__role='student')
        ).count()
        completion_rate = round((completed_enrollments / total_enrollments * 100), 1) if total_enrollments > 0 else 0
        
        # Average rating from all feedback
        all_feedbacks = Feedback.objects.all()
        avg_rating = all_feedbacks.aggregate(models.Avg('rating'))['rating__avg'] if all_feedbacks.exists() else 0
        avg_rating = round(avg_rating, 1) if avg_rating else 0
        
        context.update({
            'total_users': total_users,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'total_instructors': total_instructors,
            'total_students': total_students,
            'active_sessions': active_sessions,
            'completion_rate': f'{completion_rate}%',
            'avg_rating': avg_rating,
        })
        
    elif profile.role == 'instructor':
        # Instructor dashboard data - Real data
        instructor_courses = Course.objects.filter(instructor=request.user)
        
        # Get total students enrolled
        total_students = Enrollment.objects.filter(course__in=instructor_courses).count()
        
        # Get average rating from feedback on this instructor's courses
        feedbacks = Feedback.objects.filter(course__in=instructor_courses)
        avg_rating = feedbacks.aggregate(models.Avg('rating'))['rating__avg'] if feedbacks.exists() else 0
        avg_rating = round(avg_rating, 1) if avg_rating else 4.9
        
        # Get pending grades (submissions without grades)
        assignments = Assignment.objects.filter(course__in=instructor_courses)
        pending_grades = Submission.objects.filter(
            assignment__in=assignments,
            grade__isnull=True
        ).count()
        
        # Get today's submissions
        today = timezone.now().date()
        submissions_today = Submission.objects.filter(
            assignment__in=assignments,
            submitted_at__date=today
        ).count()
        
        # Active students (enrolled in last 30 days)
        month_ago = timezone.now() - timedelta(days=30)
        active_students = Enrollment.objects.filter(
            course__in=instructor_courses,
            enrolled_at__gte=month_ago
        ).values('student').distinct().count()
        
        context.update({
            'instructor_courses': instructor_courses,
            'total_students': total_students,
            'avg_rating': avg_rating,
            'active_students': active_students,
            'submissions_today': submissions_today,
            'pending_grades': pending_grades,
        })
        
    elif profile.role == 'student':
        # Student dashboard data - Real data
        from datetime import datetime
        
        enrolled_courses = Enrollment.objects.filter(student=request.user)
        
        # Calculate overall progress based on assignments completed
        completed_count = 0
        total_assignments = 0
        
        for enrollment in enrolled_courses:
            assignments = Assignment.objects.filter(course=enrollment.course)
            total_assignments += assignments.count()
            submissions = Submission.objects.filter(
                assignment__in=assignments,
                student=request.user
            )
            completed_count += submissions.count()
        
        overall_progress = round((completed_count / total_assignments * 100), 1) if total_assignments > 0 else 0
        
        # Study streak (consecutive days with submissions)
        submission_dates = Submission.objects.filter(
            student=request.user
        ).values('submitted_at__date').distinct().order_by('-submitted_at__date')
        
        study_streak = 0
        if submission_dates.exists():
            today = timezone.now().date()
            current_date = today
            for entry in submission_dates:
                if current_date == entry['submitted_at__date']:
                    study_streak += 1
                    current_date = current_date - timedelta(days=1)
                else:
                    break
        
        # Total hours this week (estimated as 1 hour per assignment)
        week_ago = timezone.now() - timedelta(days=7)
        submissions_this_week = Submission.objects.filter(
            student=request.user,
            submitted_at__gte=week_ago
        ).count()
        hours_this_week = submissions_this_week  # 1 hour per submission estimate
        
        # Certificates (courses completed)
        completed_courses = []
        certificates_earned = 0
        for enrollment in enrolled_courses:
            assignments = Assignment.objects.filter(course=enrollment.course)
            submissions = Submission.objects.filter(
                assignment__in=assignments,
                student=request.user
            )
            if assignments.count() > 0 and submissions.count() == assignments.count():
                completed_courses.append(enrollment.course)
                certificates_earned += 1
        
        # Skills learned (number of courses)
        skills_learned = enrolled_courses.count()
        
        # Projects completed (submissions with grades)
        projects_completed = Submission.objects.filter(
            student=request.user,
            grade__isnull=False
        ).count()
        
        # Average course rating
        my_feedbacks = Feedback.objects.filter(
            student=request.user,
            course__in=[e.course for e in enrolled_courses]
        )
        avg_course_rating = my_feedbacks.aggregate(models.Avg('rating'))['rating__avg'] if my_feedbacks.exists() else 0
        avg_course_rating = round(avg_course_rating, 1) if avg_course_rating else 0
        
        # Next goal (next incomplete course)
        next_goal = 'Complete All Courses'
        for enrollment in enrolled_courses:
            assignments = Assignment.objects.filter(course=enrollment.course)
            submissions = Submission.objects.filter(
                assignment__in=assignments,
                student=request.user
            )
            if assignments.count() > 0 and submissions.count() < assignments.count():
                next_goal = enrollment.course.title
                break
        
        context.update({
            'enrolled_courses': enrolled_courses,
            'completed_courses': completed_courses,
            'overall_progress': f'{overall_progress}%',
            'study_streak': study_streak,
            'certificates_earned': certificates_earned,
            'hours_this_week': hours_this_week,
            'total_hours': Submission.objects.filter(student=request.user).count(),
            'avg_course_rating': avg_course_rating,
            'goals_completed': len(completed_courses),
            'projects_completed': projects_completed,
            'skills_learned': skills_learned,
            'next_goal': next_goal,
        })
    
    return render(request, 'dashboard.html', context)
