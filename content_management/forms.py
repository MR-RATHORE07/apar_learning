from django import forms
from .models import Content, StudentNote

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'content_type', 'file', 'url', 'video_url', 'text_content', 'description', 'order', 'duration', 'is_required']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'text_content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Enter text content here...'}),
            'order': forms.NumberInput(attrs={'min': 0}),
            'duration': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Duration in minutes'}),
        }

class StudentNoteForm(forms.ModelForm):
    class Meta:
        model = StudentNote
        fields = ['note_text']
        widgets = {
            'note_text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write your notes here...',
                'class': 'note-textarea'
            }),
        }