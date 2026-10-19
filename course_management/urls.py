from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('my/', views.my_courses, name='my_courses'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
]