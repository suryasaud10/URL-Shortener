from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ShortURL

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CustomShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_key', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }