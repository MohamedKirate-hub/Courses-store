from django import forms
from item.models import Feedback
from .models import Section, Lecture

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content', 'rate']
        widgets = {
            'rate': forms.NumberInput(attrs={
                'min': 1, 'max':5
            })
        }

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            'title',
            'video', 'pdf',
            'duration'
        ]

    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        pdf = cleaned_data.get('pdf')
        if not video and not pdf:
                raise forms.ValidationError('You must upload either a video or a PDF.')
        if video and pdf:
             raise forms.ValidationError(
                  'A lecture can contain a video OR a PDF, not both.'
             )
        return cleaned_data