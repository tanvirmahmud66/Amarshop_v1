from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'password1', 'password2')