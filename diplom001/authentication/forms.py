from django import forms
from django.contrib.auth.forms import UserCreationForm

from authentication.models import  User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Your name')
    last_name = forms.CharField(max_length=30, required=False, help_text='Your last name')
    email = forms.EmailField(max_length=254, help_text='Your email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')