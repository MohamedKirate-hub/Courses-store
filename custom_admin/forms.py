from django import forms
from item.models import Course

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        price = cleaned_data.get('price')

        if title and len(title) < 5:
            self.add_error(
                'title',
                'Title must contain at least 5 characters.'
            )
        if price is not None and price < 0:
            self.add_error(
                'title',
                'Title must contain at least 5 characters.'
            )
        return cleaned_data
