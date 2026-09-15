from django import forms
from account_auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
            'bio'
        ]