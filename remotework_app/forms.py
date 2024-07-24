from django import forms
from.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name', 'role','join_date')

class LoginForm(forms.Form):
     email = forms.CharField(max_length=255)
     password = forms.CharField(label='Password', widget=forms.PasswordInput)