from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/assignment/create/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('course/<int:course_id>/quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/attempt/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
]