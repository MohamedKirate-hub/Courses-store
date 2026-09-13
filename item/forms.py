from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    new_topic = forms.CharField(max_length=150, required=False)
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'price', 'image', 'topics', 'language'
        ]
        widgets = {
            'topics': forms.CheckboxSelectMultiple(),
        }

    def clean_language(self):
        language = self.cleaned_data.get('language')
        if language:
            return language.strip().capitalize()
        return language