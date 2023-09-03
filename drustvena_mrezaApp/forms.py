from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Objava

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Objava
        fields = ['sadrzaj', 'privacy', 'category']  # Include the new 'category' field