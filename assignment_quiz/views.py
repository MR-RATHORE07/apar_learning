from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Assignment, Submission, Quiz, Question, QuizAttempt, Answer
from .forms import AssignmentForm, SubmissionForm, GradeForm, QuizForm, QuestionForm
from course_management.models import Course, Enrollment

@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AssignmentForm()
    return render(request, 'create_assignment.html', {'form': form, 'course': course})

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    # Verify student is enrolled in the course
    if not Enrollment.objects.filter(student=request.user, course=assignment.course).exists():
        if request.user.profile.role == 'student':
            messages.error(request, 'You must be enrolled in this course to submit an assignment.')
            return redirect('course_list')
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('course_detail', course_id=assignment.course.id)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SubmissionForm()
    return render(request, 'submit_assignment.html', {'form': form, 'assignment': assignment})

@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, assignment__course__instructor=request.user)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Submission graded successfully!')
            return redirect('course_detail', course_id=submission.assignment.course.id)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = GradeForm(instance=submission)
    return render(request, 'grade_submission.html', {'form': form, 'submission': submission})

@login_required
def create_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = QuizForm()
    return render(request, 'create_quiz.html', {'form': form, 'course': course})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    # Verify student is enrolled
    if not Enrollment.objects.filter(student=request.user, course=quiz.course).exists():
        if request.user.profile.role == 'student':
            messages.error(request, 'You must be enrolled in this course to take the quiz.')
            return redirect('course_list')
    
    if request.method == 'POST':
        attempt, created = QuizAttempt.objects.get_or_create(
            quiz=quiz,
            student=request.user,
            defaults={'started_at': timezone.now()}
        )
        score = 0
        total = questions.count()
        
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            is_correct = selected == question.correct_answer
            if is_correct:
                score += 1
            Answer.objects.get_or_create(
                attempt=attempt,
                question=question,
                defaults={'selected_answer': selected or '', 'is_correct': is_correct}
            )
        
        attempt.score = (score / total * 100) if total > 0 else 0
        attempt.completed_at = timezone.now()
        attempt.save()
        messages.success(request, f'Quiz completed! Your score: {attempt.score:.1f}%')
        return redirect('quiz_result', attempt_id=attempt.id)
    
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    answers = attempt.answers.all()
    return render(request, 'quiz_result.html', {'attempt': attempt, 'answers': answers})
