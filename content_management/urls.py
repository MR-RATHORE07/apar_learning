from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/content/add/', views.add_content, name='add_content'),
    path('content/<int:content_id>/', views.content_detail, name='content_detail'),
    path('content/<int:content_id>/save-note/', views.save_note, name='save_note'),
]