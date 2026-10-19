from django.db import models
from django.contrib.auth.models import User
from course_management.models import Course
from django.utils import timezone
from datetime import timedelta

class Assignment(models.Model):

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    
    # Enhanced fields
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    allow_late_submission = models.BooleanField(default=True)
    late_submission_penalty = models.DecimalField(max_digits=3, decimal_places=2, default=0, help_text="Penalty percentage (0-100)")
    instructions = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ['-due_date']

    def __str__(self):
        return self.title

    def is_overdue(self):
        return timezone.now() > self.due_date

    def get_submissions_by_student(self, student):
        return self.submissions.filter(student=student)


class Submission(models.Model):

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
        ('pending', 'Pending Review'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    
    # Enhanced fields
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    is_late = models.BooleanField(default=False)
    graded_at = models.DateTimeField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.student.username} - {self.assignment.title}'

    def save(self, *args, **kwargs):
        # Automatically mark late submissions
        if self.submitted_at and self.assignment.due_date:
            self.is_late = self.submitted_at > self.assignment.due_date
            if self.is_late:
                self.status = 'late'
        super().save(*args, **kwargs)


class Quiz(models.Model):

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.DurationField(blank=True, null=True)  # Duration field
    
    # Enhanced fields
    max_attempts = models.PositiveIntegerField(default=1, help_text="0 for unlimited attempts")
    shuffle_questions = models.BooleanField(default=False)
    shuffle_options = models.BooleanField(default=False)
    show_results_immediately = models.BooleanField(default=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    pass_score = models.DecimalField(max_digits=5, decimal_places=2, default=60, help_text="Minimum score to pass (%)")
    total_points = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_question_count(self):
        return self.questions.count()

    def get_average_score(self):
        attempts = self.attempts.filter(score__isnull=False)
        if attempts.exists():
            from django.db.models import Avg
            return attempts.aggregate(Avg('score'))['score__avg']
        return 0


class Question(models.Model):

    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES, default='mcq')
    options = models.JSONField()  # list of options
    correct_answer = models.CharField(max_length=500)  # the correct option
    
    # Enhanced fields
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    explanation = models.TextField(blank=True, null=True, help_text="Explanation shown after answer")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['order']

    def __str__(self):
        return self.question_text[:50]


class QuizAttempt(models.Model):

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('submitted', 'Submitted'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    
    # Enhanced fields
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    attempt_number = models.PositiveIntegerField(default=1)
    time_taken = models.DurationField(blank=True, null=True, help_text="Time taken to complete")
    is_passed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"
        ordering = ['-started_at']
        unique_together = ['quiz', 'student', 'attempt_number']

    def __str__(self):
        return f'{self.student.username} - {self.quiz.title} (Attempt {self.attempt_number})'

    def finish_quiz(self):
        self.completed_at = timezone.now()
        self.status = 'completed'
        self.time_taken = self.completed_at - self.started_at
        self.save()

    def calculate_score(self):
        """Calculate score based on correct answers"""
        correct_answers = self.answers.filter(is_correct=True)
        self.score = sum([answer.question.points for answer in correct_answers])
        self.is_passed = self.score >= self.quiz.pass_score
        self.save()


class Answer(models.Model):

    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    
    # Enhanced fields
    answer_text = models.TextField(blank=True, null=True, help_text="For essay/short answer questions")
    graded = models.BooleanField(default=False, help_text="For manual grading questions")
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f'{self.attempt} - {self.question}'
