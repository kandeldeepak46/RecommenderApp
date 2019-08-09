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

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    


class ProfileForm(forms.ModelForm):
    role = forms.CharField(label='Role', widget=forms.Select(choices=ROLE_CHOICES))
    
    class Meta:
        model = Profile
        fields = ['role']

        
