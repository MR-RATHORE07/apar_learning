from django.urls import path
from . import views

urlpatterns = [
    path('content/<int:content_id>/complete/', views.mark_completed, name='mark_completed'),
]