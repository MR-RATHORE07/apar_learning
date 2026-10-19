from rest_framework import serializers
from .models import Assignment, Submission, Quiz, Question, QuizAttempt, Answer
from course_management.serializers import CourseSerializer
from authentication.serializers import UserSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    submission_count = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = [
            'id', 'course', 'title', 'description', 'due_date', 'file', 'max_score',
            'difficulty', 'allow_late_submission', 'late_submission_penalty',
            'instructions', 'submission_count', 'is_overdue', 'created_at', 'updated_at'
        ]

    def get_submission_count(self, obj):
        return obj.submissions.count()

    def get_is_overdue(self, obj):
        return obj.is_overdue()


class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'student', 'submitted_at', 'file', 'grade',
            'feedback', 'status', 'is_late', 'graded_at', 'graded_by'
        ]
        read_only_fields = ['student', 'submitted_at', 'is_late', 'status']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'question_text', 'question_type', 'options',
            'correct_answer', 'points', 'explanation', 'order'
        ]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    course = CourseSerializer(read_only=True)
    question_count = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            'id', 'course', 'title', 'description', 'time_limit', 'max_attempts',
            'shuffle_questions', 'shuffle_options', 'show_results_immediately',
            'difficulty', 'pass_score', 'total_points', 'questions', 'question_count',
            'average_score', 'created_at', 'updated_at'
        ]

    def get_question_count(self, obj):
        return obj.get_question_count()

    def get_average_score(self, obj):
        return obj.get_average_score()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id', 'attempt', 'question', 'selected_answer', 'answer_text',
            'is_correct', 'graded', 'marks_obtained'
        ]


class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'student', 'score', 'started_at', 'completed_at',
            'status', 'attempt_number', 'time_taken', 'is_passed', 'answers'
        ]


class QuizAttemptDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for viewing quiz attempt results"""
    answers = AnswerSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'score', 'started_at', 'completed_at', 'status',
            'attempt_number', 'time_taken', 'is_passed', 'percentage', 'answers'
        ]

    def get_percentage(self, obj):
        if obj.score and obj.quiz.total_points:
            return round((obj.score / obj.quiz.total_points) * 100, 2)
        return 0
