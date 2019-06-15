from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm

from pymongo import MongoClient

# client = MongoClient("mongodb://110.34.31.28:27017")



# Create your views here.

def register(request):
    print("yo")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account is created {username}') 
            return redirect('index') 
    else:
        form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {'form': form, 'profile_form': profile_form})




# Accounts (Backup)

# Abin qwer@1234

