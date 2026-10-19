from rest_framework import routers
from django.urls import path, include
from course_management.api_views import CourseViewSet, EnrollmentViewSet
from assignment_quiz.api_views import AssignmentViewSet, SubmissionViewSet, QuizViewSet, QuestionViewSet, QuizAttemptViewSet, AnswerViewSet
from content_management.api_views import ContentViewSet
from communication.api_views import MessageViewSet
from feedback.api_views import FeedbackViewSet

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'quiz-attempts', QuizAttemptViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
