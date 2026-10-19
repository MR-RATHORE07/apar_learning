from django.contrib import admin
from .models import Assignment, Submission, Quiz, Question, QuizAttempt, Answer

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizAttempt)
admin.site.register(Answer)
