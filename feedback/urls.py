from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/feedback/', views.submit_feedback, name='submit_feedback'),
]