from django import forms
from item.models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content', 'rate']
        widgets = {
            'rate': forms.NumberInput(attrs={
                'min': 1, 'max':5
            })
        }
