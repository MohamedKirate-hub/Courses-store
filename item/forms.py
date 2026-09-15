from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    field_order = [
        'title', 
        'image', 
        'description', 
        'price', 
        'topics', 
        'new_topic', 
        'language', 
        'published'
    ]
    new_topic = forms.CharField(max_length=150, required=False)
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'price', 'image', 'topics', 'language',
            'published'
        ]
        widgets = {
            'topics': forms.CheckboxSelectMultiple(),
        }

    def clean_language(self):
        language = self.cleaned_data.get('language')
        if language:
            return language.strip().capitalize()
        return language