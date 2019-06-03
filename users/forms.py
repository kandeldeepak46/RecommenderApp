from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


FRUIT_CHOICES= [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
    ]

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    favorite_fruit= forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'favorite_fruit']