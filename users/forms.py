from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . models import Profile

ROLE_CHOICES= [
    ('Customer', 'Customer'),
    ('Shopkeeper', 'Shopkeeper'), 
    ]

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.CharField(label='Do you want to sign in as customer or shopkeeper?', widget=forms.Select(choices=ROLE_CHOICES))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']